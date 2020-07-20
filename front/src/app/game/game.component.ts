import { Component, OnInit } from '@angular/core';
import {GameService} from '../../services/game.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  image: string;
  yearGuess: number;
  score: number;
  currentRound: number;
  buttonDisabled: boolean;

  constructor(private gameService: GameService, private router: Router) {
    this.buttonDisabled = true;
    this.gameService.score$.subscribe(score => this.score = score);
    this.gameService.currentRound$.subscribe(round => this.currentRound = round);
    this.gameService.currentImage$.subscribe(path => this.image = path);
    this.gameService.getNextImage().then(data => this.buttonDisabled = false);
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    if (this.yearGuess == null) { return; }
    this.buttonDisabled = true;
    this.gameService.getScore(this.yearGuess).then(guessResult => this.gameService.score$.next(this.score + guessResult.score));
    this.yearGuess = null;
    if (this.currentRound < 10) {
      this.gameService.currentRound$.next(this.currentRound + 1);
      this.gameService.getNextImage().then(data => this.buttonDisabled = false);
    } else {
      this.router.navigate(['./result/']);
    }
  }
}
