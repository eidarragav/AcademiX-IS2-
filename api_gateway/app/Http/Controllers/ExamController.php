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
        
        $course_exist = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("COURSES_ENDPOINT")."/".$request->course_id);

        if($course_exist->status() == 404){
            return [
                "mensaje" => "el curso no existe"
            ];
        };

        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->post(env("EXAMS_EVALUATIONS_ENDPOINT"),[
            "title" => $request->title,
            "course_id" => $request->course_id,
            "passing_score" => $request->passing_score
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ]; 
    }

    public function update_exam(Request $request, $id){

    }

    public function delete_exam($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->delete(env("EXAMS_EVALUATIONS_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];  
    }
}
