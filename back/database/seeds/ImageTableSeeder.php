<?php

use Illuminate\Database\Seeder;

class ImageTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $url = 'http://127.0.0.1:8000/storage/img/';

        #1
        $france_champion = new \App\Image();
        $france_champion->year = 1998;
        $france_champion->path = $url . 'france_champions.jpg';
        $france_champion->save();

        #2
        $attentas = new \App\Image();
        $attentas->year = 1998;
        $attentas->path = $url . 'attentats_ambasseades_americaines.jpg';
        $attentas->save();
    }
}
