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
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("QUESTIONS_EVALUATIONS_ENDPOINT"));

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function create_question(){
        $exam_exist = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("EXAMS_EVALUATIONS_ENDPOINT")."/".$request->exam_id);

        if($exam_exist->status() == 404){
            return [
                "mensaje" => "el examen no existe"
            ];
        };

        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->post(env("QUESTIONS_EVALUATIONS_ENDPOINT"),[
            "exam_id" => $request->exam_id,
            "option_a" => $request->option_a,
            "option_b" => $request->option_b,
            "option_c" => $request->option_c,
            "option_d" => $request->option_d,
            "correct_option" => $request->correct_option
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ]; 
    }

    public function update_question(){

    }

    public function delete_question(){

    }
}
