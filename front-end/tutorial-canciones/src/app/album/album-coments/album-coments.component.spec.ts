import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlbumComentsComponent } from './album-coments.component';

describe('AlbumComentsComponent', () => {
  let component: AlbumComentsComponent;
  let fixture: ComponentFixture<AlbumComentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AlbumComentsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AlbumComentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
