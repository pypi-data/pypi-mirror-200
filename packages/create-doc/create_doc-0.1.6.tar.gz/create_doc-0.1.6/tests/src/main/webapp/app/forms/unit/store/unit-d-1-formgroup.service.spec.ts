import { TestBed } from '@angular/core/testing';
import { HttpResponse } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MissingTranslationHandler, TranslateModule, TranslateService } from '@ngx-translate/core';
import { missingTranslationHandler } from 'app/config/translation.config';
import { expect } from '@jest/globals';

import { UnitStoreService } from './unit-store.service';

describe('UnitStoreService', () => {
  let service: UnitStoreService;
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
      providers: [TranslateService, UnitStoreService],
    });
    service = TestBed.inject(UnitStoreService);
    translateService = TestBed.inject(TranslateService);
    translateService.setDefaultLang('en');
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
