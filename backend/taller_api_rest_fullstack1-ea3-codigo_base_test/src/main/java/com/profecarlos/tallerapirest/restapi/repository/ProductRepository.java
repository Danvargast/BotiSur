package com.profecarlos.tallerapirest.restapi.repository;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import com.profecarlos.tallerapirest.restapi.model.Product;

public interface ProductRepository extends JpaRepository<Product, Integer> {
    
    // Buscar productos por ID de categoría
    List<Product> findByCategoriaId(int categoriaId);
    
    // Buscar productos por nombre de categoría
    List<Product> findByCategoriaNombre(String nombreCategoria);
    
    // Consulta personalizada: productos de categorías activas
    @Query("SELECT p FROM Product p WHERE p.categoria.activa = true")
    List<Product> findProductosDeCategoriasActivas();
    
    // Buscar productos en un rango de precio de una categoría específica
    @Query("SELECT p FROM Product p WHERE p.categoria.id = :categoriaId AND p.precio BETWEEN :precioMin AND :precioMax")
    List<Product> findByCategoriasAndPrecioRange(@Param("categoriaId") int categoriaId, 
                                                @Param("precioMin") double precioMin, 
                                                @Param("precioMax") double precioMax);
}