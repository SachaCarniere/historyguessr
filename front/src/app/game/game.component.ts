import { Component, OnInit } from '@angular/core';
import {GameService} from '../../services/game.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  images = [];

  yearGuess: number;

  score: any = '';

  constructor(private gameService: GameService, private router: Router){
    this.gameService.getNextImage().then(path => this.images.push(path));

  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    this.gameService.getScore(this.yearGuess).then( guessResult => this.score = guessResult.score);
  }
}
