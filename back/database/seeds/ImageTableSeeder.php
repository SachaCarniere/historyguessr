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
        #1
        $france_champion = new \App\Image();
        $france_champion->year = 1998;
        $france_champion->path = 'france_champions.jpg';
        $france_champion->save();

        #2
        $attentas = new \App\Image();
        $attentas->year = 1998;
        $attentas->path = 'attentats_ambasseades_americaines.jpg';
        $attentas->save();

        #3
        $dix950 = new \App\Image();
        $dix950->year = 1950;
        $dix950->path = '1594804892.479353.jpg';
        $dix950->save();

        #4
        $dix951 = new \App\Image();
        $dix951->year = 1951;
        $dix951->path = '1594804894.870202.jpg';
        $dix951->save();

        #5
        $dix952 = new \App\Image();
        $dix952->year = 1952;
        $dix952->path = '1594804897.159037.jpg';
        $dix952->save();
    }
}
