import {HttpClient} from "@angular/common/http";
import {BaseService} from "./service";

export class GameService extends BaseService{

  private url;
  public currentGameId;

  constructor(private http: HttpClient) {
    super();
    this.url = super.getBaseUrl() + "game/";
  }

  public newGame(){
    this.http.post(this.url, null)
      .subscribe(response => {
        this.currentGameId = response["id"];
      })
  }
}
