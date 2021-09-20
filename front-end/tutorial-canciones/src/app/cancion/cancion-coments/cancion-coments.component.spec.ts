import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CancionComentsComponent } from './cancion-coments.component';

describe('CancionComentsComponent', () => {
  let component: CancionComentsComponent;
  let fixture: ComponentFixture<CancionComentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CancionComentsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CancionComentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
