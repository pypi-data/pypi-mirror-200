import { Component } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { IUnit } from 'app/entities/products/unit/unit.model';
import { UnitStoreService } from 'app/forms/unit/store/unit-store.service';
import { Unit$D$1FormGroupService } from 'app/forms/unit/store/unit-d-1-formgroup.service';

@Component({
  selector: 'jhi-unit-d-1',
  templateUrl: './unit-d-1.component.html',
})
export class Unit$D$1Component {
  isSaving = false;

  constructor(public store: UnitStoreService, public fg: Unit$D$1FormGroupService) {}

  previousState(): void {
    this.fg.cancelEdit();
  }

  save(): void {
    this.isSaving = true;
    this.subscribeToSaveResponse(this.fg.save$());
  }

  protected subscribeToSaveResponse(result: Observable<HttpResponse<IUnit>>): void {
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
