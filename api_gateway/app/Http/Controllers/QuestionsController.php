<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class QuestionsController extends Controller
{
    public function index_question(){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("QUESTIONS_EVALUATIONS_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function index_questions(){

    }

    public function create_question(){

    }

    public function update_question(){

    }

    public function delete_question(){

    }
}
