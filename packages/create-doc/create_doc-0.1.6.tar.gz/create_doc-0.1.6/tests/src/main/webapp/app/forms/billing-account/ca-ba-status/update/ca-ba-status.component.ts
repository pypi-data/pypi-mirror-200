import { Component } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { IServiceAccount } from 'app/entities/customers/service-account/service-account.model';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';
import { CaBaBasicInfoFormGroupService } from 'app/forms/billing-account/store/ca-ba-basic-info-formgroup.service';

@Component({
  selector: 'jhi-ca-ba-status',
  templateUrl: './ca-ba-status.component.html',
})
export class CaBaStatusComponent {
  isSaving = false;

  constructor(public store: BillingAccountStoreService, public fg: CaBaBasicInfoFormGroupService) {}

  previousState(): void {
    this.fg.cancelEdit();
  }

  save(): void {
    this.isSaving = true;
    this.subscribeToSaveResponse(this.fg.save$());
  }

  protected subscribeToSaveResponse(result: Observable<HttpResponse<IServiceAccount>>): void {
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
