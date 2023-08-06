import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { FormBuilder } from '@angular/forms';
import { Observable, Subscription } from 'rxjs';
import { TranslateService } from '@ngx-translate/core';
import { map, tap } from 'rxjs/operators';
import { andRsql } from 'app/shared/util/request-util';
import dayjs from 'dayjs/esm';

import { IPersonBillingAccount, PersonBillingAccount } from 'app/entities/customers/person-billing-account/person-billing-account.model';
import { PersonBillingAccountService } from 'app/entities/customers/person-billing-account/service/person-billing-account.service';
import { EventManager, EventWithContent } from 'app/core/util/event-manager.service';
import { IPerson } from 'app/entities/customers/person/person.model';
import { PersonService } from 'app/entities/customers/person/service/person.service';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';
import { IBillingAccount } from '../../../entities/customers/billing-account/billing-account.model';

@Injectable()
export class BABAAssignedPersonDetFormGroupService {
  personSuggestions: IPerson[] = [];

  editForm = this.fb.group({
    id: [],
    status: [],
    validFrom: [],
    validUntil: [],
    person: [],
    billingAccount: [],
  });
  private oldRecord?: IPersonBillingAccount;
  private statusChangesSubscription?: Subscription;
  private isEdited = false;
  public hasCurrentRecord = false;

  constructor(
    protected eventManager: EventManager,
    protected translateService: TranslateService,
    protected personBillingAccountService: PersonBillingAccountService,
    protected personService: PersonService,
    protected fb: FormBuilder,
    public store: BillingAccountStoreService
  ) {
    this.eventManager.subscribe('BABillingAccountAssignedPersonsRecordChange', event => {
      if (typeof event !== 'string') {
        if (event.content) {
          this.hasCurrentRecord = true;
          this.oldRecord = event.content as IPersonBillingAccount;
          this.updateForm(event.content as IPersonBillingAccount);
        } else {
          this.hasCurrentRecord = false;
        }
      }
    });
    this.eventManager.subscribe('BABillingAccountAssignedPersonsSaveRecord', () => {
      this.save$().subscribe();
    });
  }

  updateForm(personBillingAccount: IPersonBillingAccount): void {
    this.editForm.reset();
    this.isEdited = false;
    this.subscribeToFormStatusChanges();
    this.editForm.patchValue({
      id: personBillingAccount.id,
      status: personBillingAccount.status,
      validFrom: personBillingAccount.validFrom ? personBillingAccount.validFrom.toDate() : null,
      validUntil: personBillingAccount.validUntil ? personBillingAccount.validUntil.toDate() : null,
      person: personBillingAccount.person,
      billingAccount: personBillingAccount.billingAccount,
    });

    // Disabled fields
    this.editForm.get('status')?.disable({ onlySelf: true });
    this.editForm.get('validFrom')?.disable({ onlySelf: true });
    this.editForm.get('validUntil')?.disable({ onlySelf: true });
  }

  createFromForm(): IPersonBillingAccount {
    return {
      ...new PersonBillingAccount(),
      id: this.editForm.get(['id'])!.value,
      status: this.editForm.get(['status'])!.value,
      validFrom: this.editForm.get(['validFrom'])!.value ? dayjs(this.editForm.get(['validFrom'])!.value) : undefined,
      validUntil: this.editForm.get(['validUntil'])!.value ? dayjs(this.editForm.get(['validUntil'])!.value) : undefined,
      person: this.editForm.get(['person'])!.value,
      billingAccount: this.editForm.get(['billingAccount'])!.value,
    };
  }

  save$(): Observable<HttpResponse<IPersonBillingAccount>> {
    const personBillingAccount = this.createFromForm();
    if (personBillingAccount.id !== undefined) {
      return this.personBillingAccountService.update(personBillingAccount).pipe(
        tap((res: HttpResponse<IPersonBillingAccount>) => {
          this.eventManager.broadcast(
            new EventWithContent<IPersonBillingAccount | undefined>('BABillingAccountAssignedPersonsRecordUpdated', res.body ?? undefined)
          );
        })
      );
    }
    return this.personBillingAccountService.create(personBillingAccount).pipe(
      tap((res: HttpResponse<IPersonBillingAccount>) => {
        this.eventManager.broadcast(
          new EventWithContent<IPersonBillingAccount | undefined>('BABillingAccountAssignedPersonsRecordUpdated', res.body ?? undefined)
        );
      })
    );
  }

  cancelEdit(): void {
    if (this.oldRecord) {
      this.updateForm(this.oldRecord);
      if (this.oldRecord.id === undefined) {
        this.eventManager.broadcast('BABillingAccountAssignedPersonsCancelAddNew');
      } else {
        this.eventManager.broadcast('BABillingAccountAssignedPersonsCancelEdit');
      }
    }
  }

  subscribeToFormStatusChanges(): void {
    this.statusChangesSubscription = this.editForm.statusChanges.subscribe(() => {
      if (!this.editForm.pristine) {
        this.isEdited = true;
        this.unsubscribeFromFormStatusChanges();
        this.eventManager.broadcast('BABillingAccountAssignedPersonsIsEdited');
      }
    });
  }

  unsubscribeFromFormStatusChanges(): void {
    if (this.statusChangesSubscription) {
      this.statusChangesSubscription.unsubscribe();
    }
  }

  searchPerson($event: any): void {
    const billingAccount: IBillingAccount = this.editForm.controls['billingAccount'].value ?? { id: -7654 };
    const initialFilter = `dfltCompany==${billingAccount?.company?.id ?? -9876}`;

    let filter = '';
    if ($event.query) {
      filter = `(name=*"*${$event.query as string}*" or code=*"*${$event.query as string}*")`;
    }
    filter = andRsql(initialFilter, filter);
    this.personService
      .lov({ filter, sort: ['name,asc'] })
      .pipe(map((res: HttpResponse<IPerson[]>) => res.body ?? []))
      .subscribe((items: IPerson[]) => {
        this.personSuggestions = items;
      });
  }
}
