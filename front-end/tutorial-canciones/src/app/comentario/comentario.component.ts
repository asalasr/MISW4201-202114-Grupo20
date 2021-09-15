import { Component, OnInit ,Input, Output, EventEmitter } from '@angular/core';
import { Comentario } from './comentario';
import { Router, ActivatedRoute } from '@angular/router';
import { Album } from '../album/album';

@Component({
  selector: 'app-comentario',
  templateUrl: './comentario.component.html',
  styleUrls: ['./comentario.component.css']
})
export class ComentarioComponent implements OnInit {

  @Input() album: Album;
  @Output() userComment = new EventEmitter();

  userId: number;
  token: string;

  constructor(private router: ActivatedRoute) { }

  ngOnInit() {
    this.userId = parseInt(this.router.snapshot.params.userId)
    this.token = this.router.snapshot.params.userToken
  }

  goToDeleteComentario(){
  }

  goToCreateComentario(){
  }

  viewSectionComentario(){
    this.userComment.emit(this.album.id)
  }

}
