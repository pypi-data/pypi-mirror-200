// png-table:1.0
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { UserRouteAccessService } from 'app/core/auth/user-route-access.service';
import { UnitComponent } from '../list/unit.component';
import { Unit$TComponent } from '../unit-t/layout/unit-t.component';

const unitRoute: Routes = [
  {
    path: '',
    component: UnitComponent,
    data: {
      defaultSort: 'id,asc',
    },
    canActivate: [UserRouteAccessService],
  },
  {
    path: 'unit-t/',
    component: Unit$TComponent,
    canActivate: [UserRouteAccessService],
  },
];

@NgModule({
  imports: [RouterModule.forChild(unitRoute)],
  exports: [RouterModule],
})
export class UnitRoutingModule {}
