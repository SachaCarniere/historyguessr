export class GuessResult {
  public guess: number;
  public actualYear: number;
  public score: number;

  constructor(guess: number, actualYear: number, score: number) {
    this.guess = guess;
    this.actualYear = actualYear;
    this.score = score;
  }
}
