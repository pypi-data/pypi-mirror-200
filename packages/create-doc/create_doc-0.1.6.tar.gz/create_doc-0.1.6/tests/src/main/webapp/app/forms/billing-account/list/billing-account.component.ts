import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild } from '@angular/core';
import { HttpHeaders, HttpResponse } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { combineLatest, Subscription } from 'rxjs';
import { ConfirmationService, LazyLoadEvent } from 'primeng/api';
import { Table } from 'primeng/table';
import { TranslateService } from '@ngx-translate/core';

import { IBillingAccount, BillingAccount } from 'app/entities/customers/billing-account/billing-account.model';

import { ITEMS_PER_PAGE } from 'app/config/pagination.constants';
import { andRsql, filterToRsql, getTableSort } from 'app/shared/util/request-util';
import { BillingAccountService } from 'app/entities/customers/billing-account/service/billing-account.service';
import { EventManager, EventWithContent } from 'app/core/util/event-manager.service';
import { DataUtils } from 'app/core/util/data-util.service';
import { IListOfEnumItem } from 'app/shared/common-types/ilist-of-enum-item';
import { IParty } from 'app/entities/customers/party/party.model';
import { PartyService } from 'app/entities/customers/party/service/party.service';
import { ICustomerAccount } from 'app/entities/customers/customer-account/customer-account.model';
import { CustomerAccountService } from 'app/entities/customers/customer-account/service/customer-account.service';
import { IGeoStruct } from 'app/entities/customers/geo-struct/geo-struct.model';
import { GeoStructService } from 'app/entities/customers/geo-struct/service/geo-struct.service';
import { IPerson } from 'app/entities/customers/person/person.model';
import { PersonService } from 'app/entities/customers/person/service/person.service';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';
import dayjs from 'dayjs/esm';
import { StandardRecordStatus } from 'app/entities/enumerations/standard-record-status.model';
import { BreadcrumbService } from 'app/layouts/main/breadcrumb.service';
import { GlobalContextService } from 'app/shared/global-context/global-context.service';

@Component({
  selector: 'jhi-billing-account',
  templateUrl: './billing-account.component.html',
})
export class BillingAccountComponent implements OnInit, OnDestroy {
  @ViewChild('billingAccountTable', { static: false })
  billingAccountTable!: Table;

  @Output() currentRecord = new EventEmitter<IBillingAccount>();

  @Input()
  set tag(tag: any) {
    this.parentTag = tag;
  }

  public parentTag?: any;
  public _parentRecord?: ICustomerAccount;
  public currentRowIndex = 0;
  public _currentRecord?: IBillingAccount;
  public selectedRecord?: IBillingAccount;
  public tableFilters: any = {};
  public tableSort: string[] = [];
  public isEditing = false;
  public initialFilter = 'status==#ACTIVE#';
  public routeFilter = '';
  public globalSearchTerm = '';
  public selectedAll = false;
  public filterTypes: any = {
    name: 'string',
    description: 'string',
    formattedAddressLin: 'string',
    code: 'string',
  };

  partiesSharedCollection: IParty[] = [];
  customerAccountsSharedCollection: ICustomerAccount[] = [];
  geoStructsSharedCollection: IGeoStruct[] = [];
  peopleSharedCollection: IPerson[] = [];
  standardRecordStatusesSharedCollection: IListOfEnumItem[] = [];

  billingAccounts: IBillingAccount[] = [];
  eventSubscriptions: Subscription[] = [];
  isLoading = false;
  totalItems = 0;
  itemsPerPage = ITEMS_PER_PAGE;
  loading = true;
  page?: number;
  predicate = 'id';
  ascending = true;
  ngbPaginationPage = 1;
  addingNewRecord = false;
  showForm = true;

  constructor(
    protected billingAccountService: BillingAccountService,
    protected activatedRoute: ActivatedRoute,
    protected router: Router,
    protected dataUtils: DataUtils,
    protected translateService: TranslateService,
    protected eventManager: EventManager,
    protected confirmationService: ConfirmationService,
    protected partyService: PartyService,
    protected customerAccountService: CustomerAccountService,
    protected geoStructService: GeoStructService,
    protected personService: PersonService,
    public store: BillingAccountStoreService,
    private breadcrumbService: BreadcrumbService,
    private globalContextService: GlobalContextService
  ) {}

  setBreadcrumb(): void {
    this.breadcrumbService.setItems([
      { label: this.translateService.instant('global.menu.home') },
      {
        label: this.translateService.instant('global.menu.entities.billingAccount'),
        routerLink: ['billing-account'],
      },
    ]);
  }

  setParentRecord(parentRecord: ICustomerAccount | undefined): void {
    if (parentRecord) {
      this.showForm = true;
    } else {
      this.billingAccounts = [];
      this.ngbPaginationPage = 1;
      this.selectFirstRow();

      this.showForm = false;
      return;
    }

    if (this._parentRecord?.id) {
      if (parentRecord.id !== this._parentRecord.id) {
        this.currentRowIndex = 0;
      }
    }
    this._parentRecord = parentRecord;

    this.loadPage(1);
  }

  loadPage(page?: number, dontNavigate?: boolean, keepCurrentRecord?: boolean): void {
    this.isLoading = true;
    this.isEditing = false;
    this.addingNewRecord = false;
    const pageToLoad: number = page ?? this.page ?? 1;

    this.billingAccountService
      .query({
        filter: this.getFilter(),
        page: pageToLoad - 1,
        size: this.itemsPerPage,
        sort: this.sort(),
      })
      .subscribe(
        (res: HttpResponse<IBillingAccount[]>) => {
          this.isLoading = false;
          this.onSuccess(res.body, res.headers, pageToLoad, !dontNavigate, keepCurrentRecord);
        },
        () => {
          this.isLoading = false;
          this.onError();
        }
      );
  }

  ngOnInit(): void {
    this.setBreadcrumb();

    this.translateService.onLangChange.subscribe((/* params: LangChangeEvent */) => {
      this.setBreadcrumb();
    });

    this.routeFilter = this.activatedRoute.snapshot.queryParamMap.get('filter') ?? '';

    if (this.globalContextService.customerAccount) {
      this.setParentRecord(this.globalContextService.customerAccount);
    } else {
      this.handleNavigation();
    }

    this.eventSubscriptions.push(
      this.eventManager.subscribe('GlobalContextCustomerAccountChange', event => {
        if (typeof event !== 'string') {
          this.setParentRecord(event.content as ICustomerAccount);
        }
      })
    );

    if (!this._parentRecord) {
      this.eventManager.broadcast('ShowSetOrgContent');
    }

    this.eventSubscriptions.push(
      this.eventManager.subscribe('BillingAccountRecordUpdated', event => {
        if (typeof event !== 'string') {
          if (event.content) {
            Object.assign(this._currentRecord, event.content as IBillingAccount);
          }
          // after add new record remove the last record
          if (this.billingAccounts.length > this.itemsPerPage) {
            this.billingAccounts = this.billingAccounts.slice(0, this.itemsPerPage);
          }
          if (this.addingNewRecord && this.billingAccounts[0].id !== undefined) {
            this.addingNewRecord = false;
          }
          // broadcast RecordChange event
          this.onRowSelect();
        }
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('BillingAccountCancelAddNew', () => {
        this.removeNewRecord();
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('BillingAccountIsEdited', () => {
        this.isEditing = true;
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('BillingAccountCancelEdit', () => {
        this.isEditing = false;
      })
    );
  }

  ngOnDestroy(): void {
    this.eventSubscriptions.forEach(sub => {
      this.eventManager.destroy(sub);
    });
  }

  onLazyLoadEvent(event: LazyLoadEvent): void {
    // const queryParams = lazyLoadEventToRouterQueryParams(event, this.filtersDetails);
    // this.router.navigate(['//billing-account'], { queryParams });
    this.tableFilters = event.filters;
    this.itemsPerPage = event.rows ?? ITEMS_PER_PAGE;
    if (event.rows && event.first && event.rows > 0 && event.first > 0) {
      this.page = Math.floor(event.first / event.rows) + 1;
    } else {
      this.page = 1;
    }
    this.tableSort = getTableSort(event.multiSortMeta);
    this.loadPage();
  }

  trackId(index: number, item: IBillingAccount): number {
    return item.id!;
  }

  byteSize(base64String: string): string {
    return this.dataUtils.byteSize(base64String);
  }

  openFile(base64String: string, contentType: string | null | undefined): void {
    return this.dataUtils.openFile(base64String, contentType);
  }

  private getFilter(): string {
    const predefinedFilter = andRsql(this.initialFilter, this.routeFilter);
    let completeFilter = andRsql(this.getFilterForParentRecord(), predefinedFilter);
    const filter = filterToRsql(this.tableFilters, ['code', 'name'], this.filterTypes);
    completeFilter = andRsql(completeFilter, filter);
    return completeFilter;
  }

  private getFilterForParentRecord(): string {
    if (this._parentRecord?.id) {
      return `customerAccount.id==${this._parentRecord.id}`;
    }
    return 'id==-9876';
  }

  delete(billingAccount: IBillingAccount): void {
    this.confirmationService.confirm({
      header: this.translateService.instant('entity.delete.title'),
      message: this.translateService.instant('aportalApp.billingAccount.delete.question', { id: billingAccount.id }),
      rejectIcon: 'pi pi-ban',
      rejectLabel: this.translateService.instant('entity.action.cancel'),
      rejectButtonStyleClass: 'p-button-secondary',
      acceptIcon: 'pi pi-check',
      acceptLabel: this.translateService.instant('entity.action.delete'),
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        if (billingAccount.id) {
          this.billingAccountService.delete(billingAccount.id).subscribe(() => {
            this.loadPage();
          });
        } else {
          this.removeNewRecord();
        }
      },
    });
  }

  protected sort(): string[] {
    let hasId = false;
    for (let i = 0; i < this.tableSort.length; i++) {
      const s = this.tableSort[i];
      if (s.startsWith('id')) {
        hasId = true;
      }
    }
    if (!hasId) {
      this.tableSort.push('id');
    }
    return this.tableSort;
  }

  protected handleNavigation(): void {
    combineLatest([this.activatedRoute.data, this.activatedRoute.queryParamMap]).subscribe(([data, params]) => {
      const page = params.get('page');
      const pageNumber = page !== null ? +page : 1;
      const sort = params.get('sort') ?? data['defaultSort'];
      if (pageNumber !== this.page || !this.tableSort.includes(sort)) {
        if (sort) {
          this.tableSort.push(sort);
        }
        this.loadPage(pageNumber, true);
      }
    });
  }

  protected onSuccess(
    data: IBillingAccount[] | null,
    headers: HttpHeaders,
    page: number,
    navigate: boolean,
    keepCurrentRecord?: boolean
  ): void {
    this.totalItems = Number(headers.get('X-Total-Count'));
    this.page = page;
    const queryParams: { page: number; size: number; sort: string; filter?: string } = {
      page: this.page,
      size: this.itemsPerPage,
      sort: this.predicate + ',' + (this.ascending ? 'asc' : 'desc'),
    };
    if (this.routeFilter.length > 0) {
      queryParams.filter = this.routeFilter;
    }

    this.billingAccounts = data ?? [];
    this.ngbPaginationPage = this.page;
    this.selectFirstRow();
    if (navigate) {
      this.router.navigate(['/billing-account'], {
        queryParams,
      });
    }
  }

  protected onError(): void {
    this.ngbPaginationPage = this.page ?? 1;
  }

  /*
  selectRow(tableRow: IBillingAccount): void {
    if (this._currentRecord && this._currentRecord.id === tableRow.id) {
      return;
    }
    this._currentRecord = tableRow;
    this.onRowSelect();
  }
*/

  selectFirstRow(): void {
    if (this.billingAccounts.length > 0) {
      this._currentRecord = this.billingAccounts[0];
    } else {
      this._currentRecord = undefined;
    }
    this.selectedRecord = this._currentRecord;
    this.onRowSelect();
  }

  onRowSelect(): void {
    this.isEditing = false;
    this.currentRecord.emit(this._currentRecord);
    this.eventManager.broadcast(new EventWithContent<IBillingAccount | undefined>('BillingAccountRecordChange', this._currentRecord));
  }

  selectCurrentRecord(): void {
    let recordIsChanged = true;
    if (this.billingAccounts.length > 0) {
      if (this.selectedRecord?.id) {
        this._currentRecord = this.billingAccounts.find(item => item.id === this.selectedRecord!.id);
        if (JSON.stringify(this._currentRecord) === JSON.stringify(this.selectedRecord)) {
          recordIsChanged = false;
        }
      } else {
        this._currentRecord = this.billingAccounts[0];
      }
    } else {
      this._currentRecord = undefined;
    }
    if (recordIsChanged) {
      this.onRowSelect();
    }
  }

  selectRow(): void {
    if (this.isEditing) {
      this.confirmationService.confirm({
        header: this.translateService.instant('entity.save.title'),
        message: this.translateService.instant('entity.save.message'),
        rejectIcon: 'pi pi-ban',
        rejectLabel: this.translateService.instant('entity.action.cancel'),
        rejectButtonStyleClass: 'p-button-secondary',
        acceptIcon: 'pi pi-save',
        acceptLabel: this.translateService.instant('entity.action.save'),
        acceptButtonStyleClass: 'p-button-primary',
        accept: () => {
          this.selectedRecord = this._currentRecord;
          this.eventManager.broadcast('BillingAccountSaveRecord');
        },
        reject: () => {
          this._currentRecord = this.selectedRecord;
          this.onRowSelect();
        },
      });
    } else {
      this._currentRecord = this.selectedRecord;
      this.onRowSelect();
    }
  }

  createRecord(): void {
    // create a new record and make it a current record
    const newRecord: IBillingAccount = new BillingAccount();
    newRecord.status = StandardRecordStatus.ACTIVE;
    newRecord.validFrom = dayjs();
    newRecord.validUntil = dayjs(new Date(2200, 1, 1));
    // apply linked fields
    if (this._parentRecord?.id) {
      newRecord.customerAccount = { ...this._parentRecord };
    }
    if (this._parentRecord?.company?.id) {
      newRecord.company = this._parentRecord.company;
    }

    this.billingAccounts.unshift(newRecord);
    this.addingNewRecord = true;
    this.selectFirstRow();
  }

  removeNewRecord(): void {
    if (this.billingAccounts.length > 0) {
      if (this.billingAccounts[0].id === undefined) {
        this.billingAccounts = this.billingAccounts.slice(1);
        this.addingNewRecord = false;
        this.selectFirstRow();
      }
    }
  }

  globalSearch(): void {
    this.billingAccountTable.filterGlobal(this.globalSearchTerm, 'contains');
  }

  onSelectAllClick(): void {
    this.selectedAll = !this.selectedAll;
  }
}
// table:1.4 | list | entity-management.component | angular
