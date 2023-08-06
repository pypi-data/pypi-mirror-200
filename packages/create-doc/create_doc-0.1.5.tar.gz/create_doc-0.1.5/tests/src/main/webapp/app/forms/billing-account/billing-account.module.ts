import { NgModule } from '@angular/core';

import { SharedModule } from 'app/shared/shared.module';
import { BillingAccountRoutingModule } from './route/billing-account-routing.module';
import { BillingAccountComponent } from 'app/forms/billing-account/list/billing-account.component';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';
import { BATabsComponent } from 'app/forms/billing-account/ba-tabs/layout/ba-tabs.component';
import { BABillingAccountComponent } from 'app/forms/billing-account/ba-billing-account/layout/ba-billing-account.component';
import { BABillingAccountBasicInfoComponent } from 'app/forms/billing-account/ba-billing-account-basic-info/update/ba-billing-account-basic-info.component';
import { BABillingAccountBasicInfoFormGroupService } from 'app/forms/billing-account/store/ba-billing-account-basic-info-formgroup.service';
import { BABillingAccount$adrComponent } from 'app/forms/billing-account/ba-billing-account-adr/update/ba-billing-account-adr.component';
import { BABillingAccountStatusComponent } from 'app/forms/billing-account/ba-billing-account-status/update/ba-billing-account-status.component';
import { BABillingAccountAssignedPersonsComponent } from 'app/forms/billing-account/ba-billing-account-assigned-persons/list/ba-billing-account-assigned-persons.component';
import { BABAAssignedPersonTabComponent } from 'app/forms/billing-account/baba-assigned-person-tab/layout/baba-assigned-person-tab.component';
import { BABAAssignedPersonDetComponent } from 'app/forms/billing-account/baba-assigned-person-det/update/baba-assigned-person-det.component';
import { BABAAssignedPersonDetFormGroupService } from 'app/forms/billing-account/store/baba-assigned-person-det-formgroup.service';
import { BABAAssignedPersonRolesComponent } from 'app/forms/billing-account/baba-assigned-person-roles/list/baba-assigned-person-roles.component';
import { BABAAssignedPersonRoleDetComponent } from 'app/forms/billing-account/baba-assigned-person-role-det/update/baba-assigned-person-role-det.component';
import { BABAAssignedPersonRoleDetFormGroupService } from 'app/forms/billing-account/store/baba-assigned-person-role-det-formgroup.service';
import { CAServiceAccountsComponent } from 'app/forms/billing-account/ca-service-accounts/list/ca-service-accounts.component';
import { CaBaTabsComponent } from 'app/forms/billing-account/ca-ba-tabs/layout/ca-ba-tabs.component';
import { CaBaAccordtionComponent } from 'app/forms/billing-account/ca-ba-accordtion/layout/ca-ba-accordtion.component';
import { CaBaBasicInfoComponent } from 'app/forms/billing-account/ca-ba-basic-info/update/ca-ba-basic-info.component';
import { CaBaBasicInfoFormGroupService } from 'app/forms/billing-account/store/ca-ba-basic-info-formgroup.service';
import { CaBaStatusComponent } from 'app/forms/billing-account/ca-ba-status/update/ca-ba-status.component';

@NgModule({
  imports: [SharedModule, BillingAccountRoutingModule],
  declarations: [
    BillingAccountComponent,
    BATabsComponent,
    BABillingAccountComponent,
    BABillingAccountBasicInfoComponent,
    BABillingAccount$adrComponent,
    BABillingAccountStatusComponent,
    BABillingAccountAssignedPersonsComponent,
    BABAAssignedPersonTabComponent,
    BABAAssignedPersonDetComponent,
    BABAAssignedPersonRolesComponent,
    BABAAssignedPersonRoleDetComponent,
    CAServiceAccountsComponent,
    CaBaTabsComponent,
    CaBaAccordtionComponent,
    CaBaBasicInfoComponent,
    CaBaStatusComponent,
  ],
  entryComponents: [],
  providers: [
    BillingAccountStoreService,
    BABillingAccountBasicInfoFormGroupService,
    BABAAssignedPersonDetFormGroupService,
    BABAAssignedPersonRoleDetFormGroupService,
    CaBaBasicInfoFormGroupService,
  ],
})
export class BillingAccountModule {}
// png-table | entity-mangement.module | v2.0
