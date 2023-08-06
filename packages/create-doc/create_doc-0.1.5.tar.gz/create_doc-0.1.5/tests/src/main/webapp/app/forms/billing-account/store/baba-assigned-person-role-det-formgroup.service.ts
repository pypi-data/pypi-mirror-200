import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { FormBuilder } from '@angular/forms';
import { Observable, Subscription } from 'rxjs';
import { TranslateService } from '@ngx-translate/core';
import { map, tap } from 'rxjs/operators';
import { andRsql } from 'app/shared/util/request-util';
import dayjs from 'dayjs/esm';

import {
  IPersonBaAssignedRoles,
  PersonBaAssignedRoles,
} from 'app/entities/customers/person-ba-assigned-roles/person-ba-assigned-roles.model';
import { PersonBaAssignedRolesService } from 'app/entities/customers/person-ba-assigned-roles/service/person-ba-assigned-roles.service';
import { EventManager, EventWithContent } from 'app/core/util/event-manager.service';
import { IAccountRole } from 'app/entities/customers/account-role/account-role.model';
import { AccountRoleService } from 'app/entities/customers/account-role/service/account-role.service';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';

@Injectable()
export class BABAAssignedPersonRoleDetFormGroupService {
  orgroleSuggestions: IAccountRole[] = [];

  editForm = this.fb.group({
    id: [],
    status: [],
    validFrom: [],
    validUntil: [],
    billingAccount: [],
    orgrole: [],
    personBa: [],
  });
  private oldRecord?: IPersonBaAssignedRoles;
  private statusChangesSubscription?: Subscription;
  private isEdited = false;
  public hasCurrentRecord = false;

  constructor(
    protected eventManager: EventManager,
    protected translateService: TranslateService,
    protected personBaAssignedRolesService: PersonBaAssignedRolesService,
    protected accountRoleService: AccountRoleService,
    protected fb: FormBuilder,
    public store: BillingAccountStoreService
  ) {
    this.eventManager.subscribe('BABAAssignedPersonRolesRecordChange', event => {
      if (typeof event !== 'string') {
        if (event.content) {
          this.hasCurrentRecord = true;
          this.oldRecord = event.content as IPersonBaAssignedRoles;
          this.updateForm(event.content as IPersonBaAssignedRoles);
        } else {
          this.hasCurrentRecord = false;
        }
      }
    });
    this.eventManager.subscribe('BABAAssignedPersonRolesSaveRecord', () => {
      this.save$().subscribe();
    });
  }

  updateForm(personBaAssignedRoles: IPersonBaAssignedRoles): void {
    this.editForm.reset();
    this.isEdited = false;
    this.subscribeToFormStatusChanges();
    this.editForm.patchValue({
      id: personBaAssignedRoles.id,
      status: personBaAssignedRoles.status,
      validFrom: personBaAssignedRoles.validFrom ? personBaAssignedRoles.validFrom.toDate() : null,
      validUntil: personBaAssignedRoles.validUntil ? personBaAssignedRoles.validUntil.toDate() : null,
      billingAccount: personBaAssignedRoles.billingAccount,
      orgrole: personBaAssignedRoles.orgrole,
      personBa: personBaAssignedRoles.personBa,
    });

    // Disabled fields
    this.editForm.get('status')?.disable({ onlySelf: true });
    this.editForm.get('validFrom')?.disable({ onlySelf: true });
    this.editForm.get('validUntil')?.disable({ onlySelf: true });
  }

  createFromForm(): IPersonBaAssignedRoles {
    return {
      ...new PersonBaAssignedRoles(),
      id: this.editForm.get(['id'])!.value,
      status: this.editForm.get(['status'])!.value,
      validFrom: this.editForm.get(['validFrom'])!.value ? dayjs(this.editForm.get(['validFrom'])!.value) : undefined,
      validUntil: this.editForm.get(['validUntil'])!.value ? dayjs(this.editForm.get(['validUntil'])!.value) : undefined,
      billingAccount: this.editForm.get(['billingAccount'])!.value,
      orgrole: this.editForm.get(['orgrole'])!.value,
      personBa: this.editForm.get(['personBa'])!.value,
    };
  }

  save$(): Observable<HttpResponse<IPersonBaAssignedRoles>> {
    const personBaAssignedRoles = this.createFromForm();
    if (personBaAssignedRoles.id !== undefined) {
      return this.personBaAssignedRolesService.update(personBaAssignedRoles).pipe(
        tap((res: HttpResponse<IPersonBaAssignedRoles>) => {
          this.eventManager.broadcast(
            new EventWithContent<IPersonBaAssignedRoles | undefined>('BABAAssignedPersonRolesRecordUpdated', res.body ?? undefined)
          );
        })
      );
    }
    return this.personBaAssignedRolesService.create(personBaAssignedRoles).pipe(
      tap((res: HttpResponse<IPersonBaAssignedRoles>) => {
        this.eventManager.broadcast(
          new EventWithContent<IPersonBaAssignedRoles | undefined>('BABAAssignedPersonRolesRecordUpdated', res.body ?? undefined)
        );
      })
    );
  }

  cancelEdit(): void {
    if (this.oldRecord) {
      this.updateForm(this.oldRecord);
      if (this.oldRecord.id === undefined) {
        this.eventManager.broadcast('BABAAssignedPersonRolesCancelAddNew');
      } else {
        this.eventManager.broadcast('BABAAssignedPersonRolesCancelEdit');
      }
    }
  }

  subscribeToFormStatusChanges(): void {
    this.statusChangesSubscription = this.editForm.statusChanges.subscribe(() => {
      if (!this.editForm.pristine) {
        this.isEdited = true;
        this.unsubscribeFromFormStatusChanges();
        this.eventManager.broadcast('BABAAssignedPersonRolesIsEdited');
      }
    });
  }

  unsubscribeFromFormStatusChanges(): void {
    if (this.statusChangesSubscription) {
      this.statusChangesSubscription.unsubscribe();
    }
  }

  searchOrgrole($event: any): void {
    const initialFilter = ``;

    let filter = '';
    if ($event.query) {
      filter = `(name=*"*${$event.query as string}*" or code=*"*${$event.query as string}*")`;
    }
    filter = andRsql(initialFilter, filter);
    this.accountRoleService
      .lov({ filter, sort: ['name,asc'] })
      .pipe(map((res: HttpResponse<IAccountRole[]>) => res.body ?? []))
      .subscribe((items: IAccountRole[]) => {
        this.orgroleSuggestions = items;
      });
  }
}
