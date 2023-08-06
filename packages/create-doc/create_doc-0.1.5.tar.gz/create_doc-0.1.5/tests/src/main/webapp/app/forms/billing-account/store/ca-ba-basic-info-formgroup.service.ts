import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { FormBuilder, Validators } from '@angular/forms';
import { Observable, Subscription } from 'rxjs';
import { TranslateService } from '@ngx-translate/core';
import { map, tap } from 'rxjs/operators';
import { andRsql } from 'app/shared/util/request-util';
import dayjs from 'dayjs/esm';

import { IServiceAccount, ServiceAccount } from 'app/entities/customers/service-account/service-account.model';
import { ServiceAccountService } from 'app/entities/customers/service-account/service/service-account.service';
import { EventManager, EventWithContent } from 'app/core/util/event-manager.service';
import { DataUtils } from 'app/core/util/data-util.service';
import { IParty } from 'app/entities/customers/party/party.model';
import { PartyService } from 'app/entities/customers/party/service/party.service';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';

@Injectable()
export class CaBaBasicInfoFormGroupService {
  organizationSuggestions: IParty[] = [];

  editForm = this.fb.group({
    id: [],
    code: [null, [Validators.required]],
    name: [null, [Validators.required]],
    description: [],
    seq: [],
    status: [],
    validFrom: [],
    validUntil: [],
    formattedAddress: [],
    formattedAddressLin: [],
    customerCompanyPath: [],
    customerOrgPath: [],
    company: [null, Validators.required],
    organization: [],
    customerAccount: [null, Validators.required],
    billingAccount: [null, Validators.required],
    customerCompany: [],
    customerOrg: [],
    customerPerson: [],
  });
  private oldRecord?: IServiceAccount;
  private statusChangesSubscription?: Subscription;
  private isEdited = false;
  public hasCurrentRecord = false;

  constructor(
    protected dataUtils: DataUtils,
    protected eventManager: EventManager,
    protected translateService: TranslateService,
    protected serviceAccountService: ServiceAccountService,
    protected partyService: PartyService,
    protected fb: FormBuilder,
    public store: BillingAccountStoreService
  ) {
    this.eventManager.subscribe('CAServiceAccountsRecordChange', event => {
      if (typeof event !== 'string') {
        if (event.content) {
          this.hasCurrentRecord = true;
          this.oldRecord = event.content as IServiceAccount;
          this.updateForm(event.content as IServiceAccount);
        } else {
          this.hasCurrentRecord = false;
        }
      }
    });
    this.eventManager.subscribe('CAServiceAccountsSaveRecord', () => {
      this.save$().subscribe();
    });
  }

  updateForm(serviceAccount: IServiceAccount): void {
    this.editForm.reset();
    this.isEdited = false;
    this.subscribeToFormStatusChanges();
    this.editForm.patchValue({
      id: serviceAccount.id,
      code: serviceAccount.code,
      name: serviceAccount.name,
      description: serviceAccount.description,
      seq: serviceAccount.seq,
      status: serviceAccount.status,
      validFrom: serviceAccount.validFrom ? serviceAccount.validFrom.toDate() : null,
      validUntil: serviceAccount.validUntil ? serviceAccount.validUntil.toDate() : null,
      formattedAddress: serviceAccount.formattedAddress,
      formattedAddressLin: serviceAccount.formattedAddressLin,
      customerCompanyPath: serviceAccount.customerCompanyPath,
      customerOrgPath: serviceAccount.customerOrgPath,
      company: serviceAccount.company,
      organization: serviceAccount.organization,
      customerAccount: serviceAccount.customerAccount,
      billingAccount: serviceAccount.billingAccount,
      customerCompany: serviceAccount.customerCompany,
      customerOrg: serviceAccount.customerOrg,
      customerPerson: serviceAccount.customerPerson,
    });
  }

  createFromForm(): IServiceAccount {
    return {
      ...new ServiceAccount(),
      id: this.editForm.get(['id'])!.value,
      code: this.editForm.get(['code'])!.value,
      name: this.editForm.get(['name'])!.value,
      description: this.editForm.get(['description'])!.value,
      seq: this.editForm.get(['seq'])!.value,
      status: this.editForm.get(['status'])!.value,
      validFrom: this.editForm.get(['validFrom'])!.value ? dayjs(this.editForm.get(['validFrom'])!.value) : undefined,
      validUntil: this.editForm.get(['validUntil'])!.value ? dayjs(this.editForm.get(['validUntil'])!.value) : undefined,
      formattedAddress: this.editForm.get(['formattedAddress'])!.value,
      formattedAddressLin: this.editForm.get(['formattedAddressLin'])!.value,
      customerCompanyPath: this.editForm.get(['customerCompanyPath'])!.value,
      customerOrgPath: this.editForm.get(['customerOrgPath'])!.value,
      company: this.editForm.get(['company'])!.value,
      organization: this.editForm.get(['organization'])!.value,
      customerAccount: this.editForm.get(['customerAccount'])!.value,
      billingAccount: this.editForm.get(['billingAccount'])!.value,
      customerCompany: this.editForm.get(['customerCompany'])!.value,
      customerOrg: this.editForm.get(['customerOrg'])!.value,
      customerPerson: this.editForm.get(['customerPerson'])!.value,
    };
  }

  save$(): Observable<HttpResponse<IServiceAccount>> {
    const serviceAccount = this.createFromForm();
    if (serviceAccount.id !== undefined) {
      return this.serviceAccountService.update(serviceAccount).pipe(
        tap((res: HttpResponse<IServiceAccount>) => {
          this.eventManager.broadcast(
            new EventWithContent<IServiceAccount | undefined>('CAServiceAccountsRecordUpdated', res.body ?? undefined)
          );
        })
      );
    }
    return this.serviceAccountService.create(serviceAccount).pipe(
      tap((res: HttpResponse<IServiceAccount>) => {
        this.eventManager.broadcast(
          new EventWithContent<IServiceAccount | undefined>('CAServiceAccountsRecordUpdated', res.body ?? undefined)
        );
      })
    );
  }

  cancelEdit(): void {
    if (this.oldRecord) {
      this.updateForm(this.oldRecord);
      if (this.oldRecord.id === undefined) {
        this.eventManager.broadcast('CAServiceAccountsCancelAddNew');
      } else {
        this.eventManager.broadcast('CAServiceAccountsCancelEdit');
      }
    }
  }

  subscribeToFormStatusChanges(): void {
    this.statusChangesSubscription = this.editForm.statusChanges.subscribe(() => {
      if (!this.editForm.pristine) {
        this.isEdited = true;
        this.unsubscribeFromFormStatusChanges();
        this.eventManager.broadcast('CAServiceAccountsIsEdited');
      }
    });
  }

  unsubscribeFromFormStatusChanges(): void {
    if (this.statusChangesSubscription) {
      this.statusChangesSubscription.unsubscribe();
    }
  }

  searchOrganization($event: any): void {
    const company: IParty = this.editForm.controls['company'].value;
    const rootPartyId: number = company.id ?? -9876;
    const initialFilter = `tparty==#ORGANIZATION# and rootParty==${rootPartyId} and status==#ACTIVE#`;

    let filter = '';
    if ($event.query) {
      filter = `(name=*"*${$event.query as string}*" or code=*"*${$event.query as string}*")`;
    }
    filter = andRsql(initialFilter, filter);
    this.partyService
      .lov({ filter, sort: ['name,asc'] })
      .pipe(map((res: HttpResponse<IParty[]>) => res.body ?? []))
      .subscribe((items: IParty[]) => {
        this.organizationSuggestions = items;
      });
  }
}
