import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ComentarioComponent } from './comentario.component';

@NgModule({
  imports: [
    CommonModule
  ],
  exports:[ComentarioComponent],
  declarations: [ComentarioComponent]
})
export class ComentarioModule { }
