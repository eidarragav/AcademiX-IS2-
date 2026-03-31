<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\CoursesController;
use App\Http\Controllers\EnrollmentsController;
use App\Http\Controllers\ModulesController;
use App\Http\Controllers\LessonsController;
use App\Http\Controllers\ExamController;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});


//Autenticacion
Route::post("/register", [AuthController::class, 'register']);
Route::post("/login", [AuthController::class, 'login']);
Route::post("/logout", [AuthController::class, 'logout'])->middleware('auth:sanctum');
Route::post("/restore_password", [AuthController::class, 'restore_password']);


//Courses routes
Route::post("/courses", [CoursesController::class, 'create_course'])->middleware('auth:sanctum');
Route::get("/courses", [CoursesController::class, 'index_courses']);
Route::get("/courses/{id}", [CoursesController::class, 'index_course']);
Route::put("/courses/{id}", [CoursesController::class, 'update_course']);
Route::delete("/courses/{id}", [CoursesController::class, 'delete_course']);

//Enrollments routes
Route::post("/enrollments", [EnrollmentsController::class, 'create_enrollment'])->middleware('auth:sanctum');
Route::get("/enrollments", [EnrollmentsController::class, 'index_enrollments']);
Route::get("/enrollments/{id}", [EnrollmentsController::class, 'index_enrollment']);
Route::put("/enrollments/{id}", [EnrollmentsController::class, 'update_enrollment']);
Route::delete("/enrollments/{id}", [EnrollmentsController::class, 'delete_enrollment']);

//Modules routes
Route::post("/modules", [ModulesController::class, 'create_module']);
Route::get("/modules", [ModulesController::class, 'index_modules']);
Route::get("/modules/{id}", [ModulesController::class, 'index_module']);
Route::put("/modules/{id}", [ModulesController::class, 'update_module']);
Route::delete("/modules/{id}", [ModulesController::class, 'delete_module']);

//Lesson routes
Route::post("/lessons", [LessonsController::class, 'create_lesson']);
Route::get("/lessons", [LessonsController::class, 'index_lessons']);
Route::get("/lessons/{id}", [LessonsController::class, 'index_lesson']);
Route::put("/lessons/{id}", [LessonsController::class, 'update_lesson']);
Route::delete("/lessons/{id}", [LessonsController::class, 'delete_lesson']);

//Exams routes
Route::post("/exams", [ExamController::class, 'create_exam']);
Route::get("/exams", [ExamController::class, 'index_exams']);
Route::get("/exams/{id}", [ExamController::class, 'index_exam']);
Route::put("/exams/{id}", [ExamController::class, 'update_exam']);
Route::delete("/exams/{id}", [ExamController::class, 'delete_exam']);

//Questions routes
Route::post("/questions", [QuestionsController::class, 'create_question']);
Route::get("/questions", [QuestionsController::class, 'index_questions']);
Route::get("/questions/{id}", [QuestionsController::class, 'index_question']);
Route::put("/questions/{id}", [QuestionsController::class, 'update_question']);
Route::delete("/questions/{id}", [QuestionsController::class, 'delete_question']);
