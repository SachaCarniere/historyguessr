<?php

namespace App\Http\Controllers;

use App\Game;
use App\Image;
use App\Round;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Routing\ResponseFactory;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class ImageController extends Controller
{
    /**
     * Get random picture with same year that game ID
     *
     * @param Request $request
     * @param int $id
     * @return Image|Application|ResponseFactory|Response
     */
    public function randomImage(Request $request, int $game_id, int $round)
    {
        $game = Game::find($game_id);
        if(!$game) {
            return response('Game ID unknown', 404);
        }
        $round = $game->rounds()->where('index', $round)->first();

        if ($round->amount_unlocked == 0) {
            $images = Image::where('year', $round->year)->orderByRaw('RAND("'. $game->uuid .'")')->take(6)->get();
            foreach ($images as $key => $image) {
                $round->images()->save($image);
            }
        }

        $images = $round->images()->get();
        if ($images->count() > $round->amount_unlocked) {
            $image = $round->images()->get()[$round->amount_unlocked];
        } else {
            return response('No image available', 404);
        }

        $image->path = env('APP_URL')."storage/img/".$image->path;

        $round->amount_unlocked = $round->amount_unlocked + 1;
        $round->save();

        return $image;
    }
}
