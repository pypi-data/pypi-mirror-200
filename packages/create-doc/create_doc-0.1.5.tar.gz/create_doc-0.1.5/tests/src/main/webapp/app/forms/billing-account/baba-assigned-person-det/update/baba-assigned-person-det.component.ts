import { Component } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { IPersonBillingAccount } from 'app/entities/customers/person-billing-account/person-billing-account.model';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';
import { BABAAssignedPersonDetFormGroupService } from 'app/forms/billing-account/store/baba-assigned-person-det-formgroup.service';

@Component({
  selector: 'jhi-baba-assigned-person-det',
  templateUrl: './baba-assigned-person-det.component.html',
})
export class BABAAssignedPersonDetComponent {
  isSaving = false;

  constructor(public store: BillingAccountStoreService, public fg: BABAAssignedPersonDetFormGroupService) {}

  previousState(): void {
    this.fg.cancelEdit();
  }

  save(): void {
    this.isSaving = true;
    this.subscribeToSaveResponse(this.fg.save$());
  }

  protected subscribeToSaveResponse(result: Observable<HttpResponse<IPersonBillingAccount>>): void {
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
