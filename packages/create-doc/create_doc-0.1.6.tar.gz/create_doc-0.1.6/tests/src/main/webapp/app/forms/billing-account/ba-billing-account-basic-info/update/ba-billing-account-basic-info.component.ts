import { Component } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { IBillingAccount } from 'app/entities/customers/billing-account/billing-account.model';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';
import { BABillingAccountBasicInfoFormGroupService } from 'app/forms/billing-account/store/ba-billing-account-basic-info-formgroup.service';

@Component({
  selector: 'jhi-ba-billing-account-basic-info',
  templateUrl: './ba-billing-account-basic-info.component.html',
})
export class BABillingAccountBasicInfoComponent {
  isSaving = false;

  constructor(public store: BillingAccountStoreService, public fg: BABillingAccountBasicInfoFormGroupService) {}

  previousState(): void {
    this.fg.cancelEdit();
  }

  save(): void {
    this.isSaving = true;
    this.subscribeToSaveResponse(this.fg.save$());
  }

  protected subscribeToSaveResponse(result: Observable<HttpResponse<IBillingAccount>>): void {
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
