jest.mock('@angular/router');

import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpHeaders, HttpResponse } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { of } from 'rxjs';
import { expect } from '@jest/globals';

import { PersonBaAssignedRolesService } from 'app/entities/customers/person-ba-assigned-roles/service/person-ba-assigned-roles.service';
import { PersonBaAssignedRoles } from 'app/entities/customers/person-ba-assigned-roles/person-ba-assigned-roles.model';

import { BABAAssignedPersonRolesComponent } from './baba-assigned-person-roles.component';
import { Confirmation, ConfirmationService } from 'primeng/api';
import { MissingTranslationHandler, TranslateModule, TranslateService } from '@ngx-translate/core';
import { missingTranslationHandler } from 'app/config/translation.config';
import { BillingAccountStoreService } from 'app/forms/billing-account/store/billing-account-store.service';
import { BreadcrumbService } from 'app/layouts/main/breadcrumb.service';

describe('Component Tests', () => {
  describe('BABAAssignedPersonRoles Management Component', () => {
    let comp: BABAAssignedPersonRolesComponent;
    let fixture: ComponentFixture<BABAAssignedPersonRolesComponent>;
    let service: PersonBaAssignedRolesService;
    let confirmationService: ConfirmationService;
    let translateService: TranslateService;
    let breadcrumbService: BreadcrumbService;

    beforeEach(() => {
      TestBed.configureTestingModule({
        imports: [
          HttpClientTestingModule,
          TranslateModule.forRoot({
            missingTranslationHandler: {
              provide: MissingTranslationHandler,
              useFactory: missingTranslationHandler,
            },
          }),
        ],
        declarations: [BABAAssignedPersonRolesComponent],
        providers: [
          BillingAccountStoreService,
          ConfirmationService,
          TranslateService,
          BreadcrumbService,
          Router,
          {
            provide: ActivatedRoute,
            useValue: {
              data: of({
                defaultSort: 'id,asc',
              }),
              queryParamMap: of(
                jest.requireActual('@angular/router').convertToParamMap({
                  page: '1',
                  size: '1',
                  sort: 'id,desc',
                })
              ),
              snapshot: {
                queryParamMap: {
                  get: (param: string) => '',
                },
              },
            },
          },
        ],
      })
        .overrideTemplate(BABAAssignedPersonRolesComponent, '')
        .compileComponents();
      fixture = TestBed.createComponent(BABAAssignedPersonRolesComponent);
      comp = fixture.componentInstance;
      service = TestBed.inject(PersonBaAssignedRolesService);
      confirmationService = TestBed.inject(ConfirmationService);
      breadcrumbService = TestBed.inject(BreadcrumbService);
      translateService = TestBed.inject(TranslateService);
      translateService.setDefaultLang('en');

      const headers = new HttpHeaders().append('link', 'link;link');
      jest.spyOn(service, 'query').mockReturnValue(
        of(
          new HttpResponse({
            body: [{ id: 123 }],
            headers,
          })
        )
      );
    });

    it('Should call load all on parentRecord', () => {
      // WHEN
      comp.setParentRecord({ id: 1 });

      // THEN
      expect(service.query).toHaveBeenCalled();
      expect(comp.personBaAssignedRoles[0]).toEqual(expect.objectContaining({ id: 123 }));
    });

    it('should load a page', () => {
      // WHEN
      comp.loadPage(1);

      // THEN
      expect(service.query).toHaveBeenCalled();
      expect(comp.personBaAssignedRoles[0]).toEqual(expect.objectContaining({ id: 123 }));
    });

    it('should calculate the sort attribute for an id', () => {
      // WHEN
      comp.handleNavigation();

      // THEN
      expect(service.query).toHaveBeenCalledWith(expect.objectContaining({ sort: ['id,desc'] }));
    });

    it('should calculate the sort attribute for a non-id attribute', () => {
      // INIT
      comp.handleNavigation();

      // GIVEN
      comp.tableSort = ['name,desc'];

      // WHEN
      comp.loadPage(1);

      // THEN
      expect(service.query).toHaveBeenLastCalledWith(expect.objectContaining({ sort: ['name,desc', 'id'] }));
    });

    it('should call delete service using confirmDialog', () => {
      // GIVEN
      const confirmMethod = function (confirmation: Confirmation): ConfirmationService {
        if (confirmation.accept) {
          confirmation.accept();
        }
        return confirmationService;
      };

      jest.spyOn(confirmationService, 'confirm').mockImplementation(confirmMethod);
      jest.spyOn(service, 'delete').mockReturnValue(of(new HttpResponse({ body: {} })));

      // WHEN
      comp.delete({ id: 123 });

      // THEN
      expect(service.delete).toHaveBeenCalledWith(123);
    });
  });
});
