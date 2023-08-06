// png-table:1.0
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { UserRouteAccessService } from 'app/core/auth/user-route-access.service';
import { BillingAccountComponent } from '../list/billing-account.component';
import { BATabsComponent } from '../ba-tabs/layout/ba-tabs.component';
import { BABillingAccountComponent } from '../ba-billing-account/layout/ba-billing-account.component';
import { BABillingAccountAssignedPersonsComponent } from '../ba-billing-account-assigned-persons/list/ba-billing-account-assigned-persons.component';
import { BABAAssignedPersonTabComponent } from '../baba-assigned-person-tab/layout/baba-assigned-person-tab.component';
import { BABAAssignedPersonRolesComponent } from '../baba-assigned-person-roles/list/baba-assigned-person-roles.component';
import { CAServiceAccountsComponent } from '../ca-service-accounts/list/ca-service-accounts.component';
import { CaBaTabsComponent } from '../ca-ba-tabs/layout/ca-ba-tabs.component';
import { CaBaAccordtionComponent } from '../ca-ba-accordtion/layout/ca-ba-accordtion.component';

const billingAccountRoute: Routes = [
  {
    path: '',
    component: BillingAccountComponent,
    data: {
      defaultSort: 'id,asc',
    },
    canActivate: [UserRouteAccessService],
  },
  {
    path: 'ba-tabs/',
    component: BATabsComponent,
    canActivate: [UserRouteAccessService],
  },
  {
    path: 'ba-billing-account/',
    component: BABillingAccountComponent,
    canActivate: [UserRouteAccessService],
  },
  {
    path: 'ba-billing-account-assigned-persons/',
    component: BABillingAccountAssignedPersonsComponent,
    data: {
      defaultSort: 'id,asc',
    },
    canActivate: [UserRouteAccessService],
  },
  {
    path: 'baba-assigned-person-tab/',
    component: BABAAssignedPersonTabComponent,
    canActivate: [UserRouteAccessService],
  },
  {
    path: 'baba-assigned-person-roles/',
    component: BABAAssignedPersonRolesComponent,
    data: {
      defaultSort: 'id,asc',
    },
    canActivate: [UserRouteAccessService],
  },
  {
    path: 'ca-service-accounts/',
    component: CAServiceAccountsComponent,
    data: {
      defaultSort: 'id,asc',
    },
    canActivate: [UserRouteAccessService],
  },
  {
    path: 'ca-ba-tabs/',
    component: CaBaTabsComponent,
    canActivate: [UserRouteAccessService],
  },
  {
    path: 'ca-ba-accordtion/',
    component: CaBaAccordtionComponent,
    canActivate: [UserRouteAccessService],
  },
];

@NgModule({
  imports: [RouterModule.forChild(billingAccountRoute)],
  exports: [RouterModule],
})
export class BillingAccountRoutingModule {}
