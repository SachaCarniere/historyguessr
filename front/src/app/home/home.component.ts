import { Component, OnInit } from '@angular/core';
import {GameService} from '../../services/game.service';
import {Router} from '@angular/router';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  private uuid: string;

  constructor(private gameService: GameService, private router: Router, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.uuid = params.get('uuid');
    });
  }


  public play(): void {
    // this.gameService.currentGameId$.subscribe(id => this.router.navigate(['./game/'])); // Redirect quand l'ID est update
    if (this.uuid == null || this.uuid === '') {
      // console.log('Without uuid');
      this.gameService.newGame().then( () => this.router.navigate(['game']));
    } else {
      // console.log('With uuid');
      this.gameService.newGameWithUUID(this.uuid).then( () => this.router.navigate(['game']));
    }
  }
}
