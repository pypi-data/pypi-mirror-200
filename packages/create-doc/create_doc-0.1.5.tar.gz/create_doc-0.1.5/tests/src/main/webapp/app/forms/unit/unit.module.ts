import { NgModule } from '@angular/core';

import { SharedModule } from 'app/shared/shared.module';
import { UnitRoutingModule } from './route/unit-routing.module';
import { UnitComponent } from 'app/forms/unit/list/unit.component';
import { UnitStoreService } from 'app/forms/unit/store/unit-store.service';
import { Unit$TComponent } from 'app/forms/unit/unit-t/layout/unit-t.component';
import { Unit$D$1Component } from 'app/forms/unit/unit-d-1/update/unit-d-1.component';
import { Unit$D$1FormGroupService } from 'app/forms/unit/store/unit-d-1-formgroup.service';

@NgModule({
  imports: [SharedModule, UnitRoutingModule],
  declarations: [UnitComponent, Unit$TComponent, Unit$D$1Component],
  entryComponents: [],
  providers: [UnitStoreService, Unit$D$1FormGroupService],
})
export class UnitModule {}
// png-table | entity-mangement.module | v2.0
