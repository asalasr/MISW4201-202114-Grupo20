import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { faEdit, faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import swal from 'sweetalert2';

@Component({
  selector: 'app-album-coments',
  templateUrl: './album-coments.component.html',
  styleUrls: ['./album-coments.component.css']
})
export class AlbumComentsComponent implements OnInit {

  public faEdit: any = faEdit;
  public faTrashAlt: any = faTrashAlt;
  public formComent: FormGroup;

  constructor() { }

  ngOnInit(): void {
    this.formComent = new FormGroup({
      coment : new FormControl('', [Validators.maxLength(1000), Validators.minLength(5)])
    });
  }

  public deleteComent(): void {
    swal.fire({
      title: '¿Estas seguro de eliminar este comentario?',
      text: "",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si!',
      cancelButtonText: 'No!'
    }).then((result) => {
      if(result.isConfirmed) {
        this.ngOnInit();
        let toast = swal.mixin({
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true,
          didOpen: (toast) => {
            toast.addEventListener('mouseenter', swal.stopTimer)
            toast.addEventListener('mouseleave', swal.resumeTimer)
          }
        });
        toast.fire({
          icon: 'success',
          title: 'Comentario eliminado!'
        });
      }
    });
  }

  public saveComent(): void {
    swal.fire({
      title: '¿Estas seguro de publicar este comentario?',
      text: "",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si!',
      cancelButtonText: 'No!'
    }).then((result) => {
      if (result.isConfirmed) {
        let toast = swal.mixin({
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true,
          didOpen: (toast) => {
            toast.addEventListener('mouseenter', swal.stopTimer)
            toast.addEventListener('mouseleave', swal.resumeTimer)
          }
        });
        toast.fire({
          icon: 'success',
          title: 'Comentario publicado!'
        });
      }
    });
  }

}
