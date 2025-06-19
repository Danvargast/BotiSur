package com.profecarlos.tallerapirest.restapi.controller;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.profecarlos.tallerapirest.restapi.model.Categoria;
import com.profecarlos.tallerapirest.restapi.repository.CategoriaRepository;

@RestController
@CrossOrigin(origins = {"http://localhost:3000", "http://127.0.0.1:5500", "https://perfunlandia.cl", "file://"},
            allowedHeaders = "*",
            methods = {RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE})
@RequestMapping("/api/v1")
public class CategoriaController {
    
    @Autowired
    private CategoriaRepository categoriaRepository;
    
    @PostMapping("categoria")
    public ResponseEntity<Categoria> crearCategoria(@RequestBody Categoria categoria) {
        // Validar que no exista una categoría con el mismo nombre
        if (categoriaRepository.findByNombre(categoria.getNombre()).isPresent()) {
            return new ResponseEntity<>(HttpStatus.CONFLICT);
        }
        
        Categoria nuevaCategoria = categoriaRepository.save(categoria);
        return new ResponseEntity<>(nuevaCategoria, HttpStatus.CREATED);
    }
    
    @GetMapping("categorias")
    public ResponseEntity<List<Categoria>> obtenerTodasLasCategorias() {
        List<Categoria> categorias = categoriaRepository.findAll();
        return new ResponseEntity<>(categorias, HttpStatus.OK);
    }
    
    @GetMapping("categorias/activas")
    public ResponseEntity<List<Categoria>> obtenerCategoriasActivas() {
        List<Categoria> categoriasActivas = categoriaRepository.findByActivaTrue();
        return new ResponseEntity<>(categoriasActivas, HttpStatus.OK);
    }
    
    @GetMapping("categoria/{id}")
    public ResponseEntity<Categoria> obtenerCategoriaPorId(@PathVariable("id") int id) {
        return categoriaRepository.findById(id)
                .map(categoria -> new ResponseEntity<>(categoria, HttpStatus.OK))
                .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }
    
    @GetMapping("categoria/{id}/productos")
    public ResponseEntity<List<com.profecarlos.tallerapirest.restapi.model.Product>> obtenerProductosDeCategoria(@PathVariable("id") int id) {
        return categoriaRepository.findById(id)
                .map(categoria -> new ResponseEntity<>(categoria.getProductos(), HttpStatus.OK))
                .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }
    
    @PutMapping("categoria/{id}")
    public ResponseEntity<Categoria> actualizarCategoria(@PathVariable("id") int id, @RequestBody Categoria categoriaActualizada) {
        return categoriaRepository.findById(id)
                .map(categoriaExistente -> {
                    categoriaExistente.setNombre(categoriaActualizada.getNombre());
                    categoriaExistente.setDescripcion(categoriaActualizada.getDescripcion());
                    categoriaExistente.setActiva(categoriaActualizada.isActiva());
                    
                    Categoria categoriaGuardada = categoriaRepository.save(categoriaExistente);
                    return new ResponseEntity<>(categoriaGuardada, HttpStatus.OK);
                })
                .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }
    
    @DeleteMapping("categoria/{id}")
    public ResponseEntity<Void> eliminarCategoria(@PathVariable("id") int id) {
        return categoriaRepository.findById(id)
                .map(categoria -> {
                    // Nota: Esto eliminará todos los productos asociados debido a CascadeType.ALL
                    categoriaRepository.delete(categoria);
                    return new ResponseEntity<Void>(HttpStatus.NO_CONTENT);
                })
                .orElse(new ResponseEntity<Void>(HttpStatus.NOT_FOUND));
    }
}