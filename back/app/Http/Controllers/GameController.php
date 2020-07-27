<?php

namespace App\Http\Controllers;

use App\Game;
use App\GuessResult;
use App\Image;
use App\Round;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Routing\ResponseFactory;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Ramsey\Uuid\Uuid;

class GameController extends Controller
{
    /**
     * Show the form for creating a new resource.
     *
     * @return Game
     */
    public function create()
    {
        $game = new Game();
        $game->uuid = Uuid::uuid4();
        $game->save();

        $images_random = Image::orderByRaw('RAND()')->take(10)->get();
        foreach ($images_random as $key=>$value) {
            $round = new Round();
            $round->index = $key + 1;
            $round->year = $value->year;
            $game->rounds()->save($round);
        }

        return $game;
    }

    public function answer(Request $request, int $game_id, int $round) {
        $game = Game::find($game_id);
        if(!$game) {
            return response('Game ID unknown', 404);
        }
        $round = $game->rounds()->where('index', $round)->first();
        if ($round->year_answered != null) {
            return response('Round already answered', 403);
        }

        $round->year_answered = $request->input("guess");
        $round->save();

        return new GuessResult((int) $request->input("guess"), $round->year);
    }
}
