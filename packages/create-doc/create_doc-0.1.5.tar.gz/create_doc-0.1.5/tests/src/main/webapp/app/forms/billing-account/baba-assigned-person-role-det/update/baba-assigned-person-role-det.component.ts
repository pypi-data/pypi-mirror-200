import { Component } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { IPersonBaAssignedRoles } from 'app/entities/customers/person-ba-assigned-roles/person-ba-assigned-roles.model';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';
import { BABAAssignedPersonRoleDetFormGroupService } from 'app/forms/billing-account/store/baba-assigned-person-role-det-formgroup.service';

@Component({
  selector: 'jhi-baba-assigned-person-role-det',
  templateUrl: './baba-assigned-person-role-det.component.html',
})
export class BABAAssignedPersonRoleDetComponent {
  isSaving = false;

  constructor(public store: BillingAccountStoreService, public fg: BABAAssignedPersonRoleDetFormGroupService) {}

  previousState(): void {
    this.fg.cancelEdit();
  }

  save(): void {
    this.isSaving = true;
    this.subscribeToSaveResponse(this.fg.save$());
  }

  protected subscribeToSaveResponse(result: Observable<HttpResponse<IPersonBaAssignedRoles>>): void {
    result.pipe(finalize(() => this.onSaveFinalize())).subscribe(
      () => this.onSaveSuccess(),
      () => this.onSaveError()
    );
  }

  protected onSaveSuccess(): void {
    // this.previousState();
  }

  protected onSaveError(): void {
    // Api for inheritance.
  }

  protected onSaveFinalize(): void {
    this.isSaving = false;
  }
}
// form | v1.0
