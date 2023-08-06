import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { FormBuilder, Validators } from '@angular/forms';
import { Observable, Subscription } from 'rxjs';
import { TranslateService } from '@ngx-translate/core';
import { map, tap } from 'rxjs/operators';
import { andRsql } from 'app/shared/util/request-util';
import dayjs from 'dayjs/esm';

import { IBillingAccount, BillingAccount } from 'app/entities/customers/billing-account/billing-account.model';
import { BillingAccountService } from 'app/entities/customers/billing-account/service/billing-account.service';
import { EventManager, EventWithContent } from 'app/core/util/event-manager.service';
import { DataUtils } from 'app/core/util/data-util.service';
import { IParty } from 'app/entities/customers/party/party.model';
import { PartyService } from 'app/entities/customers/party/service/party.service';
import { IGeoStruct } from 'app/entities/customers/geo-struct/geo-struct.model';
import { GeoStructService } from 'app/entities/customers/geo-struct/service/geo-struct.service';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';

@Injectable()
export class BABillingAccountBasicInfoFormGroupService {
  organizationSuggestions: IParty[] = [];
  countrySuggestions: IGeoStruct[] = [];

  editForm = this.fb.group({
    id: [],
    code: [null, [Validators.required]],
    name: [null, [Validators.required]],
    taxIdentifier: [],
    description: [],
    seq: [],
    status: [],
    validFrom: [],
    validUntil: [],
    formattedAddress: [],
    formattedAddressLin: [],
    countryName: [],
    countyName: [],
    regionName: [],
    placeName: [],
    postNumber: [],
    postName: [],
    streetName: [],
    homeNumber: [],
    homeLetter: [],
    isGeocoded: [],
    latitude: [],
    longitude: [],
    customerCompanyPath: [],
    customerOrgPath: [],
    company: [null, Validators.required],
    organization: [],
    customerAccount: [null, Validators.required],
    country: [],
    region: [],
    place: [],
    street: [],
    post: [],
    county: [],
    customerCompany: [],
    customerOrg: [],
    customerPerson: [],
  });
  private oldRecord?: IBillingAccount;
  private statusChangesSubscription?: Subscription;
  private isEdited = false;
  public hasCurrentRecord = false;

  constructor(
    protected dataUtils: DataUtils,
    protected eventManager: EventManager,
    protected translateService: TranslateService,
    protected billingAccountService: BillingAccountService,
    protected partyService: PartyService,
    protected geoStructService: GeoStructService,
    protected fb: FormBuilder,
    public store: BillingAccountStoreService
  ) {
    this.eventManager.subscribe('BillingAccountRecordChange', event => {
      if (typeof event !== 'string') {
        if (event.content) {
          this.hasCurrentRecord = true;
          this.oldRecord = event.content as IBillingAccount;
          this.updateForm(event.content as IBillingAccount);
        } else {
          this.hasCurrentRecord = false;
        }
      }
    });
    this.eventManager.subscribe('BillingAccountSaveRecord', () => {
      this.save$().subscribe();
    });
  }

  updateForm(billingAccount: IBillingAccount): void {
    this.editForm.reset();
    this.isEdited = false;
    this.subscribeToFormStatusChanges();
    this.editForm.patchValue({
      id: billingAccount.id,
      code: billingAccount.code,
      name: billingAccount.name,
      taxIdentifier: billingAccount.taxIdentifier,
      description: billingAccount.description,
      seq: billingAccount.seq,
      status: billingAccount.status,
      validFrom: billingAccount.validFrom ? billingAccount.validFrom.toDate() : null,
      validUntil: billingAccount.validUntil ? billingAccount.validUntil.toDate() : null,
      formattedAddress: billingAccount.formattedAddress,
      formattedAddressLin: billingAccount.formattedAddressLin,
      countryName: billingAccount.countryName,
      countyName: billingAccount.countyName,
      regionName: billingAccount.regionName,
      placeName: billingAccount.placeName,
      postNumber: billingAccount.postNumber,
      postName: billingAccount.postName,
      streetName: billingAccount.streetName,
      homeNumber: billingAccount.homeNumber,
      homeLetter: billingAccount.homeLetter,
      isGeocoded: billingAccount.isGeocoded,
      latitude: billingAccount.latitude,
      longitude: billingAccount.longitude,
      customerCompanyPath: billingAccount.customerCompanyPath,
      customerOrgPath: billingAccount.customerOrgPath,
      company: billingAccount.company,
      organization: billingAccount.organization,
      customerAccount: billingAccount.customerAccount,
      country: billingAccount.country,
      region: billingAccount.region,
      place: billingAccount.place,
      street: billingAccount.street,
      post: billingAccount.post,
      county: billingAccount.county,
      customerCompany: billingAccount.customerCompany,
      customerOrg: billingAccount.customerOrg,
      customerPerson: billingAccount.customerPerson,
    });

    // Disabled fields
    this.editForm.get('status')?.disable({ onlySelf: true });
    this.editForm.get('validFrom')?.disable({ onlySelf: true });
    this.editForm.get('validUntil')?.disable({ onlySelf: true });
  }

  createFromForm(): IBillingAccount {
    return {
      ...new BillingAccount(),
      id: this.editForm.get(['id'])!.value,
      code: this.editForm.get(['code'])!.value,
      name: this.editForm.get(['name'])!.value,
      taxIdentifier: this.editForm.get(['taxIdentifier'])!.value,
      description: this.editForm.get(['description'])!.value,
      seq: this.editForm.get(['seq'])!.value,
      status: this.editForm.get(['status'])!.value,
      validFrom: this.editForm.get(['validFrom'])!.value ? dayjs(this.editForm.get(['validFrom'])!.value) : undefined,
      validUntil: this.editForm.get(['validUntil'])!.value ? dayjs(this.editForm.get(['validUntil'])!.value) : undefined,
      formattedAddress: this.editForm.get(['formattedAddress'])!.value,
      formattedAddressLin: this.editForm.get(['formattedAddressLin'])!.value,
      countryName: this.editForm.get(['countryName'])!.value,
      countyName: this.editForm.get(['countyName'])!.value,
      regionName: this.editForm.get(['regionName'])!.value,
      placeName: this.editForm.get(['placeName'])!.value,
      postNumber: this.editForm.get(['postNumber'])!.value,
      postName: this.editForm.get(['postName'])!.value,
      streetName: this.editForm.get(['streetName'])!.value,
      homeNumber: this.editForm.get(['homeNumber'])!.value,
      homeLetter: this.editForm.get(['homeLetter'])!.value,
      isGeocoded: this.editForm.get(['isGeocoded'])!.value,
      latitude: this.editForm.get(['latitude'])!.value,
      longitude: this.editForm.get(['longitude'])!.value,
      customerCompanyPath: this.editForm.get(['customerCompanyPath'])!.value,
      customerOrgPath: this.editForm.get(['customerOrgPath'])!.value,
      company: this.editForm.get(['company'])!.value,
      organization: this.editForm.get(['organization'])!.value,
      customerAccount: this.editForm.get(['customerAccount'])!.value,
      country: this.editForm.get(['country'])!.value,
      region: this.editForm.get(['region'])!.value,
      place: this.editForm.get(['place'])!.value,
      street: this.editForm.get(['street'])!.value,
      post: this.editForm.get(['post'])!.value,
      county: this.editForm.get(['county'])!.value,
      customerCompany: this.editForm.get(['customerCompany'])!.value,
      customerOrg: this.editForm.get(['customerOrg'])!.value,
      customerPerson: this.editForm.get(['customerPerson'])!.value,
    };
  }

  save$(): Observable<HttpResponse<IBillingAccount>> {
    const billingAccount = this.createFromForm();
    if (billingAccount.id !== undefined) {
      return this.billingAccountService.update(billingAccount).pipe(
        tap((res: HttpResponse<IBillingAccount>) => {
          this.eventManager.broadcast(
            new EventWithContent<IBillingAccount | undefined>('BillingAccountRecordUpdated', res.body ?? undefined)
          );
        })
      );
    }
    return this.billingAccountService.create(billingAccount).pipe(
      tap((res: HttpResponse<IBillingAccount>) => {
        this.eventManager.broadcast(
          new EventWithContent<IBillingAccount | undefined>('BillingAccountRecordUpdated', res.body ?? undefined)
        );
      })
    );
  }

  cancelEdit(): void {
    if (this.oldRecord) {
      this.updateForm(this.oldRecord);
      if (this.oldRecord.id === undefined) {
        this.eventManager.broadcast('BillingAccountCancelAddNew');
      } else {
        this.eventManager.broadcast('BillingAccountCancelEdit');
      }
    }
  }

  subscribeToFormStatusChanges(): void {
    this.statusChangesSubscription = this.editForm.statusChanges.subscribe(() => {
      if (!this.editForm.pristine) {
        this.isEdited = true;
        this.unsubscribeFromFormStatusChanges();
        this.eventManager.broadcast('BillingAccountIsEdited');
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

  searchCountry($event: any): void {
    const initialFilter = `tgeo==1`;

    let filter = '';
    if ($event.query) {
      filter = `(name=*"*${$event.query as string}*" or code=*"*${$event.query as string}*")`;
    }
    filter = andRsql(initialFilter, filter);
    this.geoStructService
      .lov({ filter, sort: ['name,asc'] })
      .pipe(map((res: HttpResponse<IGeoStruct[]>) => res.body ?? []))
      .subscribe((items: IGeoStruct[]) => {
        this.countrySuggestions = items;
      });
  }
}
