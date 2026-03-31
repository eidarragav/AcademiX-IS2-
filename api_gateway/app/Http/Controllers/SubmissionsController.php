<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class SubmissionsController extends Controller
{
    public function index_submission($id){

    }

    public function index_submissions(){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("SUBMISSIONS_EVALUATIONS_ENDPOINT"));

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function create_submission(Request $request){
        $user = auth()->user();

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
        ])->post(env("SUBMISSIONS_EVALUATIONS_ENDPOINT"),[
            "exam_id" => $request->exam_id,
            "score" => $request->score,
            "user_id" => $user->id,
            "passed" => $request->passed,
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ]; 
    }

    public function update_submission(Request $request, $id){
        $user = auth()->user();

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
        ])->put(env("SUBMISSIONS_EVALUATIONS_ENDPOINT"),[
            "exam_id" => $request->exam_id,
            "score" => $request->score,
            "user_id" => $user->id,
            "passed" => $request->passed,
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ]; 
    }

    public function delete_submission($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->delete(env("SUBMISSIONS_EVALUATIONS_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }


}
