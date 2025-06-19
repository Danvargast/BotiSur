package com.profecarlos.tallerapirest.restapi.model;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "categorias")
public class Categoria {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    
    @Column(nullable = false, unique = true, length = 100)
    private String nombre;
    
    
    @Column(nullable = false)
    private boolean activa = true;
    
    // Relación One-to-Many con Product
    @OneToMany(mappedBy = "categoria", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Product> productos;
    
    // Constructores
    public Categoria() {}
    
    public Categoria(String nombre) {
        this.nombre = nombre;
        this.activa = true;
    }
    
    // Getters y Setters
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    public String getNombre() {
        return nombre;
    }
    
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    
    
    public boolean isActiva() {
        return activa;
    }
    
    public void setActiva(boolean activa) {
        this.activa = activa;
    }
    
    public List<Product> getProductos() {
        return productos;
    }
    
    public void setProductos(List<Product> productos) {
        this.productos = productos;
    }
}