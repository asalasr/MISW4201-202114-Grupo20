import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Album } from '../album';
import { AlbumService } from '../album.service';

@Component({
  selector: 'app-album-share',
  templateUrl: './album-share.component.html',
  styleUrls: ['./album-share.component.css']
})
export class AlbumShareComponent implements OnInit {

  userId: number;
  token: string;
  albumId: number;
  album: Album;
  albumForm !: FormGroup;
  constructor(private albumService: AlbumService,
    private formBuilder: FormBuilder,
    private router: ActivatedRoute, private routerPath: Router,
    private toastr: ToastrService) { }

  ngOnInit() {
    if(!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " "){
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else{
      this.userId = parseInt(this.router.snapshot.params.userId)
      this.token = this.router.snapshot.params.userToken
      this.albumId = this.router.snapshot.params.albumId
      this.albumService.getAlbum(this.albumId)
      .subscribe(album => {
        this.album = album
        this.albumForm = this.formBuilder.group({
          nombreUsuario: [album.usuario, [Validators.required]],
          idUsuario: ["", [Validators.required]],
        })
      })

    }
  }

  compartirAlbum(){

  }

  cancelarCompatir(){
    this.albumForm.reset()
    this.routerPath.navigate([`/albumes/${this.userId}/${this.token}`])
  }

  showError(error: string){
    this.toastr.error(error, "Error")
  }

}
