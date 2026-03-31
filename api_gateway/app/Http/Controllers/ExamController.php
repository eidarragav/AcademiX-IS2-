<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ExamController extends Controller
{
    public function index_exam($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("EXAMS_EVALUATIONS_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];   
    }

    public function index_exams(){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("EXAMS_EVALUATIONS_ENDPOINT"));

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function create_exam(Request $request){

    }

    public function update_exam(Request $request, $id){

    }

    public function delete_exam($id){

    }
}
