import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { AlbumListComponent } from './album-list/album-list.component';
import { AlbumDetailComponent } from './album-detail/album-detail.component';
import { AlbumCreateComponent } from './album-create/album-create.component';
import { AlbumEditComponent } from './album-edit/album-edit.component';
import { AppHeaderModule } from '../app-header/app-header.module';
import { AlbumJoinCancionComponent } from './album-join-cancion/album-join-cancion.component';
import { AppFooterModule } from '../app-footer/app-footer.module'
import { AlbumShareComponent } from './album-share/album-share.component';
import { ComentarioModule } from '../comentario/comentario.module';




@NgModule({
    declarations: [AlbumListComponent, AlbumDetailComponent, AlbumCreateComponent, AlbumEditComponent, AlbumJoinCancionComponent, AlbumShareComponent],
  imports: [
    CommonModule, ReactiveFormsModule, AppHeaderModule, AppFooterModule,ComentarioModule
  ],
  exports:[AlbumListComponent, AlbumDetailComponent, AlbumCreateComponent, AlbumEditComponent, AlbumJoinCancionComponent, AlbumShareComponent]
})
export class AlbumModule { }
