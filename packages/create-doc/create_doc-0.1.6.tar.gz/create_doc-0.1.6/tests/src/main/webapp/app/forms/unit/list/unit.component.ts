import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild } from '@angular/core';
import { HttpHeaders, HttpResponse } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { combineLatest, Subscription } from 'rxjs';
import { ConfirmationService, LazyLoadEvent } from 'primeng/api';
import { Table } from 'primeng/table';
import { TranslateService } from '@ngx-translate/core';

import { IUnit, Unit } from 'app/entities/products/unit/unit.model';

import { ITEMS_PER_PAGE } from 'app/config/pagination.constants';
import { andRsql, filterToRsql, getTableSort } from 'app/shared/util/request-util';
import { UnitService } from 'app/entities/products/unit/service/unit.service';
import { EventManager, EventWithContent } from 'app/core/util/event-manager.service';
import { DataUtils } from 'app/core/util/data-util.service';
import { IListOfEnumItem } from 'app/shared/common-types/ilist-of-enum-item';
import { UnitStoreService } from 'app/forms/unit/store/unit-store.service';
import dayjs from 'dayjs/esm';
import { StandardRecordStatus } from 'app/entities/enumerations/standard-record-status.model';
import { BreadcrumbService } from 'app/layouts/main/breadcrumb.service';

@Component({
  selector: 'jhi-unit',
  templateUrl: './unit.component.html',
})
export class UnitComponent implements OnInit, OnDestroy {
  @ViewChild('unitTable', { static: false })
  unitTable!: Table;

  @Output() currentRecord = new EventEmitter<IUnit>();

  @Input()
  set tag(tag: any) {
    this.parentTag = tag;
  }

  public parentTag?: any;
  public _parentRecord?: any;
  public currentRowIndex = 0;
  public _currentRecord?: IUnit;
  public selectedRecord?: IUnit;
  public tableFilters: any = {};
  public tableSort: string[] = [];
  public isEditing = false;
  public initialFilter = '';
  public routeFilter = '';
  public globalSearchTerm = '';
  public selectedAll = false;
  public filterTypes: any = {
    code: 'string',
    name: 'string',
    description: 'string',
    status: 'enum',
    id: 'number',
  };

  standardRecordStatusesSharedCollection: IListOfEnumItem[] = [];

  units: IUnit[] = [];
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
    protected unitService: UnitService,
    protected activatedRoute: ActivatedRoute,
    protected router: Router,
    protected dataUtils: DataUtils,
    protected translateService: TranslateService,
    protected eventManager: EventManager,
    protected confirmationService: ConfirmationService,
    public store: UnitStoreService,
    private breadcrumbService: BreadcrumbService
  ) {}

  setBreadcrumb(): void {
    this.breadcrumbService.setItems([
      { label: this.translateService.instant('global.menu.home') },
      {
        label: this.translateService.instant('global.menu.entities.unit'),
        routerLink: ['unit'],
      },
    ]);
  }

  setParentRecord(parentRecord: any | undefined): void {
    if (parentRecord) {
      this.showForm = true;
    } else {
      this.units = [];
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

    this.unitService
      .query({
        filter: this.getFilter(),
        page: pageToLoad - 1,
        size: this.itemsPerPage,
        sort: this.sort(),
      })
      .subscribe(
        (res: HttpResponse<IUnit[]>) => {
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

    this.handleNavigation();

    this.eventSubscriptions.push(
      this.eventManager.subscribe('UnitRecordUpdated', event => {
        if (typeof event !== 'string') {
          if (event.content) {
            Object.assign(this._currentRecord, event.content as IUnit);
          }
          // after add new record remove the last record
          if (this.units.length > this.itemsPerPage) {
            this.units = this.units.slice(0, this.itemsPerPage);
          }
          if (this.addingNewRecord && this.units[0].id !== undefined) {
            this.addingNewRecord = false;
          }
          // broadcast RecordChange event
          this.onRowSelect();
        }
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('UnitCancelAddNew', () => {
        this.removeNewRecord();
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('UnitIsEdited', () => {
        this.isEditing = true;
      })
    );

    this.eventSubscriptions.push(
      this.eventManager.subscribe('UnitCancelEdit', () => {
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
    // this.router.navigate(['//unit'], { queryParams });
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

  trackId(index: number, item: IUnit): number {
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
    return '';
  }

  delete(unit: IUnit): void {
    this.confirmationService.confirm({
      header: this.translateService.instant('entity.delete.title'),
      message: this.translateService.instant('aportalApp.unit.delete.question', { id: unit.id }),
      rejectIcon: 'pi pi-ban',
      rejectLabel: this.translateService.instant('entity.action.cancel'),
      rejectButtonStyleClass: 'p-button-secondary',
      acceptIcon: 'pi pi-check',
      acceptLabel: this.translateService.instant('entity.action.delete'),
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        if (unit.id) {
          this.unitService.delete(unit.id).subscribe(() => {
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

  protected onSuccess(data: IUnit[] | null, headers: HttpHeaders, page: number, navigate: boolean, keepCurrentRecord?: boolean): void {
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

    this.units = data ?? [];
    this.ngbPaginationPage = this.page;
    this.selectFirstRow();
    if (navigate) {
      this.router.navigate(['/unit'], {
        queryParams,
      });
    }
  }

  protected onError(): void {
    this.ngbPaginationPage = this.page ?? 1;
  }

  /*
  selectRow(tableRow: IUnit): void {
    if (this._currentRecord && this._currentRecord.id === tableRow.id) {
      return;
    }
    this._currentRecord = tableRow;
    this.onRowSelect();
  }
*/

  selectFirstRow(): void {
    if (this.units.length > 0) {
      this._currentRecord = this.units[0];
    } else {
      this._currentRecord = undefined;
    }
    this.selectedRecord = this._currentRecord;
    this.onRowSelect();
  }

  onRowSelect(): void {
    this.isEditing = false;
    this.currentRecord.emit(this._currentRecord);
    this.eventManager.broadcast(new EventWithContent<IUnit | undefined>('UnitRecordChange', this._currentRecord));
  }

  selectCurrentRecord(): void {
    let recordIsChanged = true;
    if (this.units.length > 0) {
      if (this.selectedRecord?.id) {
        this._currentRecord = this.units.find(item => item.id === this.selectedRecord!.id);
        if (JSON.stringify(this._currentRecord) === JSON.stringify(this.selectedRecord)) {
          recordIsChanged = false;
        }
      } else {
        this._currentRecord = this.units[0];
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
          this.eventManager.broadcast('UnitSaveRecord');
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
    const newRecord: IUnit = new Unit();
    newRecord.status = StandardRecordStatus.ACTIVE;
    newRecord.validFrom = dayjs();
    newRecord.validUntil = dayjs(new Date(2200, 1, 1));

    this.units.unshift(newRecord);
    this.addingNewRecord = true;
    this.selectFirstRow();
  }

  removeNewRecord(): void {
    if (this.units.length > 0) {
      if (this.units[0].id === undefined) {
        this.units = this.units.slice(1);
        this.addingNewRecord = false;
        this.selectFirstRow();
      }
    }
  }

  globalSearch(): void {
    this.unitTable.filterGlobal(this.globalSearchTerm, 'contains');
  }

  onSelectAllClick(): void {
    this.selectedAll = !this.selectedAll;
  }
}
// table:1.4 | list | entity-management.component | angular
