export class GuessResult {
  public guess: number;
  public actualYear: number;
  public score: number;
  public images = [];
  public eventNames = [];
  public captions = [];

  constructor(guess: number, actualYear: number, score: number, images, eventNames, captions) {
    this.guess = guess;
    this.actualYear = actualYear;
    this.score = score;
    this.images = images;
    this.eventNames = eventNames;
    this.captions = captions;
  }
}
