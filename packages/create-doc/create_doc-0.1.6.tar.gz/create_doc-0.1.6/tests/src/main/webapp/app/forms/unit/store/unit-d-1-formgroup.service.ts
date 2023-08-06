import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { FormBuilder, Validators } from '@angular/forms';
import { Observable, Subscription } from 'rxjs';
import { TranslateService } from '@ngx-translate/core';
import { tap } from 'rxjs/operators';
import dayjs from 'dayjs/esm';

import { IUnit, Unit } from 'app/entities/products/unit/unit.model';
import { UnitService } from 'app/entities/products/unit/service/unit.service';
import { EventManager, EventWithContent } from 'app/core/util/event-manager.service';
import { DataUtils } from 'app/core/util/data-util.service';
import { UnitStoreService } from 'app/forms/unit/store/unit-store.service';

@Injectable()
export class Unit$D$1FormGroupService {
  editForm = this.fb.group({
    id: [],
    code: [null, [Validators.required]],
    name: [null, [Validators.required]],
    description: [],
    seq: [],
    status: [],
    validFrom: [],
    validUntil: [],
  });
  private oldRecord?: IUnit;
  private statusChangesSubscription?: Subscription;
  private isEdited = false;
  public hasCurrentRecord = false;

  constructor(
    protected dataUtils: DataUtils,
    protected eventManager: EventManager,
    protected translateService: TranslateService,
    protected unitService: UnitService,
    protected fb: FormBuilder,
    public store: UnitStoreService
  ) {
    this.eventManager.subscribe('UnitRecordChange', event => {
      if (typeof event !== 'string') {
        if (event.content) {
          this.hasCurrentRecord = true;
          this.oldRecord = event.content as IUnit;
          this.updateForm(event.content as IUnit);
        } else {
          this.hasCurrentRecord = false;
        }
      }
    });
    this.eventManager.subscribe('UnitSaveRecord', () => {
      this.save$().subscribe();
    });
  }

  updateForm(unit: IUnit): void {
    this.editForm.reset();
    this.isEdited = false;
    this.subscribeToFormStatusChanges();
    this.editForm.patchValue({
      id: unit.id,
      code: unit.code,
      name: unit.name,
      description: unit.description,
      seq: unit.seq,
      status: unit.status,
      validFrom: unit.validFrom ? unit.validFrom.toDate() : null,
      validUntil: unit.validUntil ? unit.validUntil.toDate() : null,
    });
  }

  createFromForm(): IUnit {
    return {
      ...new Unit(),
      id: this.editForm.get(['id'])!.value,
      code: this.editForm.get(['code'])!.value,
      name: this.editForm.get(['name'])!.value,
      description: this.editForm.get(['description'])!.value,
      seq: this.editForm.get(['seq'])!.value,
      status: this.editForm.get(['status'])!.value,
      validFrom: this.editForm.get(['validFrom'])!.value ? dayjs(this.editForm.get(['validFrom'])!.value) : undefined,
      validUntil: this.editForm.get(['validUntil'])!.value ? dayjs(this.editForm.get(['validUntil'])!.value) : undefined,
    };
  }

  save$(): Observable<HttpResponse<IUnit>> {
    const unit = this.createFromForm();
    if (unit.id !== undefined) {
      return this.unitService.update(unit).pipe(
        tap((res: HttpResponse<IUnit>) => {
          this.eventManager.broadcast(new EventWithContent<IUnit | undefined>('UnitRecordUpdated', res.body ?? undefined));
        })
      );
    }
    return this.unitService.create(unit).pipe(
      tap((res: HttpResponse<IUnit>) => {
        this.eventManager.broadcast(new EventWithContent<IUnit | undefined>('UnitRecordUpdated', res.body ?? undefined));
      })
    );
  }

  cancelEdit(): void {
    if (this.oldRecord) {
      this.updateForm(this.oldRecord);
      if (this.oldRecord.id === undefined) {
        this.eventManager.broadcast('UnitCancelAddNew');
      } else {
        this.eventManager.broadcast('UnitCancelEdit');
      }
    }
  }

  subscribeToFormStatusChanges(): void {
    this.statusChangesSubscription = this.editForm.statusChanges.subscribe(() => {
      if (!this.editForm.pristine) {
        this.isEdited = true;
        this.unsubscribeFromFormStatusChanges();
        this.eventManager.broadcast('UnitIsEdited');
      }
    });
  }

  unsubscribeFromFormStatusChanges(): void {
    if (this.statusChangesSubscription) {
      this.statusChangesSubscription.unsubscribe();
    }
  }
}
