import { TestBed } from '@angular/core/testing';
import { HttpResponse } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MissingTranslationHandler, TranslateModule, TranslateService } from '@ngx-translate/core';
import { missingTranslationHandler } from 'app/config/translation.config';

import { BillingAccountStoreService } from './billing-account-store.service';

describe('BillingAccountStoreService', () => {
  let service: BillingAccountStoreService;
  let translateService: TranslateService;

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
      providers: [TranslateService, BillingAccountStoreService],
    });
    service = TestBed.inject(BillingAccountStoreService);
    translateService = TestBed.inject(TranslateService);
    translateService.setDefaultLang('en');
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
