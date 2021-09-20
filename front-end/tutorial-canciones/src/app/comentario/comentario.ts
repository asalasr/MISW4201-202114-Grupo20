export class Comentario {
  id: number;
  comentario: string;
  fecha: string;

  constructor(
      id: number,
      comentario: string,
      fecha: string
  ){
      this.id = id,
      this.comentario = comentario,
      this.fecha = fecha
  }
}
