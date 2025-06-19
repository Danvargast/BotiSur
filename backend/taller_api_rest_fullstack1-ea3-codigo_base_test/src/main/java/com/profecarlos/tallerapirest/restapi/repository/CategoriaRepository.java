package com.profecarlos.tallerapirest.restapi.repository;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import com.profecarlos.tallerapirest.restapi.model.Categoria;

public interface CategoriaRepository extends JpaRepository<Categoria, Integer> {
    
    // Buscar categoría por nombre (útil para validaciones)
    Optional<Categoria> findByNombre(String nombre);
    
    // Buscar solo categorías activas
    List<Categoria> findByActivaTrue();
    
    // Consulta personalizada: categorías con productos
    @Query("SELECT c FROM Categoria c WHERE SIZE(c.productos) > 0")
    List<Categoria> findCategoriasConProductos();
    
    // Buscar categorías que contengan cierto texto en el nombre
    List<Categoria> findByNombreContainingIgnoreCase(String texto);
}