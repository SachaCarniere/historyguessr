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
        $game->save();

        for ($i = 0; $i < 10; $i++) {
            $round = new Round();
            $round->index = $i + 1;
            $round->year = 1998;

            $game->rounds()->save($round);
        }


        return $game;
    }

    public function answer(Request $request, int $game_id, int $round) {
        $game = Game::find($game_id);
        if(!$game) {
            return response('Game ID unknown', 404);
        }

        return new GuessResult((int) $request->input("guess"), $game->rounds()->where('index', $round)->first()->year);
    }
}
