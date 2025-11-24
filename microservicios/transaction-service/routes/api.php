<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TransactionController;

// Ruta de verificación
Route::get('/', function () {
    return response()->json([
        'mensaje' => 'Microservicio de Transacciones',
        'estado' => 'Activo',
        'fecha' => now()->toDateTimeString()
    ]);
});

// Health check
Route::get('/health', function () {
    return response()->json([
        'estado' => 'ok',
        'servicio' => 'transacciones',
        'timestamp' => now()->toISOString()
    ]);
});

// Rutas CRUD para transacciones
Route::apiResource('transacciones', TransactionController::class);