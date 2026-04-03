<?php

namespace App\Exceptions;

use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Throwable;
use Illuminate\Auth\AuthenticationException;

class Handler extends ExceptionHandler
{
    /**
     * The list of the inputs that are never flashed to the session on validation exceptions.
     *
     * @var array<int, string>
     */
    protected $dontFlash = [
        'current_password',
        'password',
        'password_confirmation',
    ];

    /**
     * Register the exception handling callbacks for the application.
     */
    public function register(): void
    {
        $this->reportable(function (Throwable $e) {
        });


        $this->renderable(function (AuthenticationException $e, $request) {
            return response()->json([
                'error' => $request->bearerToken()
                    ? 'Token inválido'
                    : 'No envió el token del usuario'
            ], 401);
        });
    }

    protected function unauthenticated($request, AuthenticationException $exception)
    {
        return response()->json([
            'error' => $request->bearerToken()
                ? 'Token inválido'
                : 'No envió el token del usuario'
        ], 401);
    }
}
