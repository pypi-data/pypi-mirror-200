import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild } from '@angular/core';
import { HttpHeaders, HttpResponse } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { combineLatest, Subscription } from 'rxjs';
import { ConfirmationService, LazyLoadEvent } from 'primeng/api';
import { Table } from 'primeng/table';
import { TranslateService } from '@ngx-translate/core';

import {
  IPersonBaAssignedRoles,
  PersonBaAssignedRoles,
} from 'app/entities/customers/person-ba-assigned-roles/person-ba-assigned-roles.model';

import { ITEMS_PER_PAGE } from 'app/config/pagination.constants';
import { andRsql, filterToRsql, getTableSort } from 'app/shared/util/request-util';
import { PersonBaAssignedRolesService } from 'app/entities/customers/person-ba-assigned-roles/service/person-ba-assigned-roles.service';
import { EventManager, EventWithContent } from 'app/core/util/event-manager.service';
import { IListOfEnumItem } from 'app/shared/common-types/ilist-of-enum-item';
import { IBillingAccount } from 'app/entities/customers/billing-account/billing-account.model';
import { BillingAccountService } from 'app/entities/customers/billing-account/service/billing-account.service';
import { IAccountRole } from 'app/entities/customers/account-role/account-role.model';
import { AccountRoleService } from 'app/entities/customers/account-role/service/account-role.service';
import { IPersonBillingAccount } from 'app/entities/customers/person-billing-account/person-billing-account.model';
import { PersonBillingAccountService } from 'app/entities/customers/person-billing-account/service/person-billing-account.service';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';
import dayjs from 'dayjs/esm';
import { StandardRecordStatus } from 'app/entities/enumerations/standard-record-status.model';

@Component({
  selector: 'jhi-baba-assigned-person-roles',
  templateUrl: './baba-assigned-person-roles.component.html',
})
export class BABAAssignedPersonRolesComponent implements OnInit, OnDestroy {
  @ViewChild('bABAAssignedPersonRolesTable', { static: true })
  bABAAssignedPersonRolesTable!: Table;

  @Output() currentRecord = new EventEmitter<IPersonBaAssignedRoles>();

  @Input()
  set tag(tag: any) {
    this.parentTag = tag;
  }

  public parentTag?: any;
  public _parentRecord?: IPersonBillingAccount;
  public currentRowIndex = 0;
  public _currentRecord?: IPersonBaAssignedRoles;
  public selectedRecord?: IPersonBaAssignedRoles;
  public tableFilters: any = {};
  public tableSort: string[] = [];
  public isEditing = false;
  public initialFilter = '';
  public routeFilter = '';
  public selectedAll = false;
  public filterTypes: any = {
    orgrole: 'relationship',
    status: 'enum',
    validFrom: 'date',
    validUntil: 'date',
  };

  billingAccountsSharedCollection: IBillingAccount[] = [];
  accountRolesSharedCollection: IAccountRole[] = [];
  personBillingAccountsSharedCollection: IPersonBillingAccount[] = [];
  standardRecordStatusesSharedCollection: IListOfEnumItem[] = [];

  personBaAssignedRoles: IPersonBaAssignedRoles[] = [];
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
    protected personBaAssignedRolesService: PersonBaAssignedRolesService,
    protected activatedRoute: ActivatedRoute,
    protected router: Router,
    protected translateService: TranslateService,
    protected eventManager: EventManager,
    protected confirmationService: ConfirmationService,
    protected billingAccountService: BillingAccountService,
    protected accountRoleService: AccountRoleService,
    protected personBillingAccountService: PersonBillingAccountService,
    public store: BillingAccountStoreService
  ) {}

  setParentRecord(parentRecord: IPersonBillingAccount | undefined): void {
    if (parentRecord) {
      this.showForm = true;
    } else {
      this.personBaAssignedRoles = [];
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

  loadPage(page?: number, dontNavigate = true, keepCurrentRecord?: boolean): void {
    this.isLoading = true;
    this.isEditing = false;
    this.addingNewRecord = false;
    const pageToLoad: number = page ?? this.page ?? 1;

    this.personBaAssignedRolesService
      .query({
        filter: this.getFilter(),
        page: pageToLoad - 1,
        size: this.itemsPerPage,
        sort: this.sort(),
      })
      .subscribe(
        (res: HttpResponse<IPersonBaAssignedRoles[]>) => {
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
    this.eventSubscriptions.push(
      this.eventManager.subscribe('BABillingAccountAssignedPersonsRecordChange', event => {
        if (typeof event !== 'string') {
          this.setParentRecord(event.content as IPersonBillingAccount);
        }
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('BABAAssignedPersonRolesRecordUpdated', event => {
        if (typeof event !== 'string') {
          if (event.content) {
            Object.assign(this._currentRecord, event.content as IPersonBaAssignedRoles);
          }
          // after add new record remove the last record
          if (this.personBaAssignedRoles.length > this.itemsPerPage) {
            this.personBaAssignedRoles = this.personBaAssignedRoles.slice(0, this.itemsPerPage);
          }
          if (this.addingNewRecord && this.personBaAssignedRoles[0].id !== undefined) {
            this.addingNewRecord = false;
          }
          // broadcast RecordChange event
          this.onRowSelect();
        }
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('BABAAssignedPersonRolesCancelAddNew', () => {
        this.removeNewRecord();
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('BABAAssignedPersonRolesIsEdited', () => {
        this.isEditing = true;
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('BABAAssignedPersonRolesCancelEdit', () => {
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
    // this.router.navigate(['/baba-assigned-person-roles'], { queryParams });
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

  trackId(index: number, item: IPersonBaAssignedRoles): number {
    return item.id!;
  }

  private getFilter(): string {
    const predefinedFilter = andRsql(this.initialFilter, this.routeFilter);
    let completeFilter = andRsql(this.getFilterForParentRecord(), predefinedFilter);
    const filter = filterToRsql(this.tableFilters, undefined, this.filterTypes);
    completeFilter = andRsql(completeFilter, filter);
    return completeFilter;
  }

  private getFilterForParentRecord(): string {
    if (this._parentRecord?.id && this._parentRecord.billingAccount?.id) {
      return `personBa.id==${this._parentRecord.id} + and + billingAccount.id==${this._parentRecord.billingAccount.id}`;
    }
    return 'id==-9876';
  }

  delete(personBaAssignedRoles: IPersonBaAssignedRoles): void {
    this.confirmationService.confirm({
      header: this.translateService.instant('entity.delete.title'),
      message: this.translateService.instant('aportalApp.bABAAssignedPersonRoles.delete.question', { id: personBaAssignedRoles.id }),
      rejectIcon: 'pi pi-ban',
      rejectLabel: this.translateService.instant('entity.action.cancel'),
      rejectButtonStyleClass: 'p-button-secondary',
      acceptIcon: 'pi pi-check',
      acceptLabel: this.translateService.instant('entity.action.delete'),
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        if (personBaAssignedRoles.id) {
          this.personBaAssignedRolesService.delete(personBaAssignedRoles.id).subscribe(() => {
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

  handleNavigation(): void {
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
    data: IPersonBaAssignedRoles[] | null,
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

    this.personBaAssignedRoles = data ?? [];
    this.ngbPaginationPage = this.page;
    this.selectFirstRow();
    if (navigate) {
      this.router.navigate(['baba-assigned-person-roles'], {
        queryParams,
      });
    }
  }

  protected onError(): void {
    this.ngbPaginationPage = this.page ?? 1;
  }

  /*
  selectRow(tableRow: IPersonBaAssignedRoles): void {
    if (this._currentRecord && this._currentRecord.id === tableRow.id) {
      return;
    }
    this._currentRecord = tableRow;
    this.onRowSelect();
  }
*/

  selectFirstRow(): void {
    if (this.personBaAssignedRoles.length > 0) {
      this._currentRecord = this.personBaAssignedRoles[0];
    } else {
      this._currentRecord = undefined;
    }
    this.selectedRecord = this._currentRecord;
    this.onRowSelect();
  }

  onRowSelect(): void {
    this.isEditing = false;
    this.currentRecord.emit(this._currentRecord);
    this.eventManager.broadcast(
      new EventWithContent<IPersonBaAssignedRoles | undefined>('BABAAssignedPersonRolesRecordChange', this._currentRecord)
    );
  }

  selectCurrentRecord(): void {
    let recordIsChanged = true;
    if (this.personBaAssignedRoles.length > 0) {
      if (this.selectedRecord?.id) {
        this._currentRecord = this.personBaAssignedRoles.find(item => item.id === this.selectedRecord!.id);
        if (JSON.stringify(this._currentRecord) === JSON.stringify(this.selectedRecord)) {
          recordIsChanged = false;
        }
      } else {
        this._currentRecord = this.personBaAssignedRoles[0];
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
          this.eventManager.broadcast('BABAAssignedPersonRolesSaveRecord');
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
    const newRecord: IPersonBaAssignedRoles = new PersonBaAssignedRoles();
    newRecord.status = StandardRecordStatus.ACTIVE;
    newRecord.validFrom = dayjs();
    newRecord.validUntil = dayjs(new Date(2200, 1, 1));
    // apply linked fields
    if (this._parentRecord?.id) {
      newRecord.personBa = { ...this._parentRecord };
    }
    if (this._parentRecord?.billingAccount?.id) {
      newRecord.billingAccount = this._parentRecord.billingAccount;
    }

    this.personBaAssignedRoles.unshift(newRecord);
    this.addingNewRecord = true;
    this.selectFirstRow();
  }

  removeNewRecord(): void {
    if (this.personBaAssignedRoles.length > 0) {
      if (this.personBaAssignedRoles[0].id === undefined) {
        this.personBaAssignedRoles = this.personBaAssignedRoles.slice(1);
        this.addingNewRecord = false;
        this.selectFirstRow();
      }
    }
  }

  onSelectAllClick(): void {
    this.selectedAll = !this.selectedAll;
  }
}
// table:1.4 | list | entity-management.component | angular
