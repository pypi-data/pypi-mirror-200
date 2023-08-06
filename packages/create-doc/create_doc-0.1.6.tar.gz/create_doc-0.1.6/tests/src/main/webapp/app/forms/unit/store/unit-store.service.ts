import { Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { IListOfEnumItem } from 'app/shared/common-types/ilist-of-enum-item';

@Injectable()
export class UnitStoreService {
  standardRecordStatusesSharedCollection: IListOfEnumItem[] = [];

  constructor(protected translateService: TranslateService) {
    this.defineEnums();
    this.translateService.onLangChange.subscribe(() => {
      this.defineEnums();
    });
  }

  defineEnums(): void {
    this.standardRecordStatusesSharedCollection = [];
    this.standardRecordStatusesSharedCollection.push({
      value: null,
      label: this.translateService.instant('aportalApp.StandardRecordStatus.null'),
    });
    this.standardRecordStatusesSharedCollection.push({
      value: 'NOT_ACTIVE',
      label: this.translateService.instant('aportalApp.StandardRecordStatus.NOT_ACTIVE'),
    });
    this.standardRecordStatusesSharedCollection.push({
      value: 'ACTIVE',
      label: this.translateService.instant('aportalApp.StandardRecordStatus.ACTIVE'),
    });
  }
}
