# Violation Fixed: Refactoring a Framework-Centric System

> This is a before/after refactor example. It shows a system that violates the Cairn canon, the specific rules broken, and how to fix them.

---

## The System: A Simple E-Commerce API

The system is a Spring Boot e-commerce API. It allows customers to place orders, view products, and check out. The original code is framework-centric, database-centric, and tightly coupled.

---

## BEFORE: The Violations

### Directory Structure (Framework-Centric)

```
ecommerce-api/
├── controllers/
│   ├── OrderController.java
│   ├── ProductController.java
│   └── CheckoutController.java
├── models/
│   ├── Order.java
│   ├── Product.java
│   └── User.java
├── repositories/
│   ├── OrderRepository.java
│   ├── ProductRepository.java
│   └── UserRepository.java
├── services/
│   ├── OrderService.java
│   ├── ProductService.java
│   └── CheckoutService.java
├── dto/
│   ├── OrderDto.java
│   └── ProductDto.java
└── EcommerceApplication.java
```

**Violations:**
- The top-level directories scream "Spring!" not "E-Commerce!" **Rule:** R-057 (Screaming Architecture).
- The structure is organized by technical layer, not by use case. **Rule:** R-039 (Use Cases Divide the System).
- This is a classic **Framework-Centric Architecture** anti-pattern.

---

### Order.java (Database-Centric, Framework in Core)

```java
// BEFORE: models/Order.java
package com.example.ecommerce.models;

import javax.persistence.*;
import java.util.List;

@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "customer_id")
    private String customerId;

    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id")
    private List<OrderLine> lines;

    @Column(name = "total")
    private double total;

    // Getters and setters...

    public void calculateTotal() {
        this.total = lines.stream()
            .mapToDouble(line -> line.getQuantity() * line.getUnitPrice())
            .sum();
    }
}
```

**Violations:**
- `@Entity`, `@Table`, `@Id`, `@GeneratedValue`, `@Column`, `@OneToMany`, `@JoinColumn` are JPA annotations. JPA is a framework. **Rule:** R-012 (No Frameworks in Core Code).
- The Entity knows about the database schema (`name = "orders"`, `name = "customer_id"`). **Rule:** R-011 (No SQL in Use Cases / Entities).
- The Entity is tied to JPA. It cannot be used without JPA. **Rule:** R-001 (Dependency Rule).
- This is a **Database-Centric Architecture** anti-pattern.

---

### OrderService.java (Business Logic Mixed with Framework)

```java
// BEFORE: services/OrderService.java
package com.example.ecommerce.services;

import com.example.ecommerce.models.Order;
import com.example.ecommerce.repositories.OrderRepository;
import com.example.ecommerce.dto.OrderDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;

    @Transactional
    public OrderDto placeOrder(OrderDto dto) {
        Order order = new Order();
        order.setCustomerId(dto.getCustomerId());
        order.setLines(dto.getLines());
        order.calculateTotal();
        orderRepository.save(order);
        return new OrderDto(order.getId(), order.getTotal());
    }
}
```

**Violations:**
- `@Service`, `@Autowired`, `@Transactional` are Spring annotations. Spring is a framework. **Rule:** R-012 (No Frameworks in Core Code).
- `OrderRepository` is a Spring Data JPA interface. The service depends on a framework-specific repository. **Rule:** R-006 (DIP: No References to Volatile Concrete Classes).
- The service accepts `OrderDto` (a web-specific data structure) as input. **Rule:** R-004 (No Outer Data Formats).
- The service mixes business logic (`calculateTotal`) with framework concerns (`@Transactional`). **Rule:** R-016 (SRP: One Actor per Module).

---

### OrderController.java (Business Logic in the Controller)

```java
// BEFORE: controllers/OrderController.java
package com.example.ecommerce.controllers;

import com.example.ecommerce.services.OrderService;
import com.example.ecommerce.dto.OrderDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/orders")
public class OrderController {
    @Autowired
    private OrderService orderService;

    @PostMapping
    public OrderDto placeOrder(@RequestBody OrderDto dto) {
        // No conversion — the controller directly passes the DTO to the service.
        return orderService.placeOrder(dto);
    }
}
```

**Violations:**
- The controller does not convert HTTP input to a simple Request Model. It passes `OrderDto` directly to the service. **Rule:** R-004 (No Outer Data Formats).
- The controller is not a Humble Object — it contains no logic, but it also does not protect the inner circles from outer-circle data formats. **Pattern:** Humble Object Pattern (violated).

---

### OrderRepository.java (Framework Interface in the Core)

```java
// BEFORE: repositories/OrderRepository.java
package com.example.ecommerce.repositories;

import com.example.ecommerce.models.Order;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<Order, Long> {
}
```

**Violations:**
- `JpaRepository` is a Spring Data JPA interface. The repository is in the "core" but depends on a framework. **Rule:** R-012 (No Frameworks in Core Code).
- The core depends on Spring Data JPA. **Rule:** R-001 (Dependency Rule).

---

## AFTER: The Fix

### Step 1: Reorganize by Use Case (Screaming Architecture)

```
ecommerce-api/
├── order_placement/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── Order.java
│   │   ├── usecases/
│   │   │   ├── PlaceOrder.java
│   │   │   ├── PlaceOrderRequest.java
│   │   │   └── PlaceOrderResponse.java
│   │   └── ports/
│   │       └── OrderRepository.java
│   ├── adapters/
│   │   ├── persistence/
│   │   │   ├── JpaOrderRepository.java
│   │   │   └── OrderEntityMapper.java
│   │   └── web/
│   │       ├── OrderController.java
│   │       ├── OrderPresenter.java
│   │       └── OrderViewModel.java
│   └── config/
│       └── OrderPlacementConfig.java
├── product_catalog/
│   └── ... (similar structure)
├── checkout/
│   └── ... (similar structure)
└── main/
    └── EcommerceApplication.java
```

**Fixes:**
- Top-level directories are now `order_placement/`, `product_catalog/`, `checkout/` — business functions. **Rule:** R-057.
- The structure screams "E-Commerce!" not "Spring!". **Rule:** R-039.

---

### Step 2: Clean the Entity (Remove Framework and Database)

```java
// AFTER: order_placement/domain/entities/Order.java
package order_placement.domain.entities;

import java.util.List;

public class Order {
    private final String id;
    private final String customerId;
    private final List<OrderLine> lines;
    private double total;

    public Order(String id, String customerId, List<OrderLine> lines) {
        this.id = id;
        this.customerId = customerId;
        this.lines = lines;
        this.total = 0.0;
    }

    public void calculateTotal() {
        this.total = lines.stream()
            .mapToDouble(line -> line.getQuantity() * line.getUnitPrice())
            .sum();
    }

    public void applyDiscount(double discountRate) {
        this.total = this.total * (1 - discountRate);
    }

    public double getTotal() {
        return total;
    }

    // Getters for id, customerId, lines...
}
```

**Fixes:**
- All JPA annotations removed. **Rule:** R-012.
- No database schema knowledge. **Rule:** R-011.
- The Entity is pure Java. It can be used without JPA. **Rule:** R-001.

---

### Step 3: Extract the Use Case (Remove Framework from Business Logic)

```java
// AFTER: order_placement/domain/usecases/PlaceOrder.java
package order_placement.domain.usecases;

import order_placement.domain.entities.Order;
import order_placement.domain.ports.OrderRepository;

public class PlaceOrder {
    private final OrderRepository orderRepository;

    public PlaceOrder(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public PlaceOrderResponse execute(PlaceOrderRequest request) {
        Order order = new Order(request.getId(), request.getCustomerId(), request.getLines());
        order.calculateTotal();
        orderRepository.save(order);
        return new PlaceOrderResponse(order.getId(), order.getTotal());
    }
}
```

```java
// AFTER: order_placement/domain/usecases/PlaceOrderRequest.java
package order_placement.domain.usecases;

import java.util.List;

public class PlaceOrderRequest {
    private final String id;
    private final String customerId;
    private final List<OrderLine> lines;

    public PlaceOrderRequest(String id, String customerId, List<OrderLine> lines) {
        this.id = id;
        this.customerId = customerId;
        this.lines = lines;
    }

    // Getters...
}
```

```java
// AFTER: order_placement/domain/usecases/PlaceOrderResponse.java
package order_placement.domain.usecases;

public class PlaceOrderResponse {
    private final String orderId;
    private final double total;

    public PlaceOrderResponse(String orderId, double total) {
        this.orderId = orderId;
        this.total = total;
    }

    // Getters...
}
```

**Fixes:**
- No Spring annotations. **Rule:** R-012.
- No `@Transactional`. Transaction management is moved to the adapter. **Rule:** R-016.
- Depends on `OrderRepository` interface, not `JpaRepository`. **Rule:** R-006.
- Uses simple Request/Response models, not `OrderDto`. **Rule:** R-004.

---

### Step 4: Define the Port (Interface in the Use Cases Layer)

```java
// AFTER: order_placement/domain/ports/OrderRepository.java
package order_placement.domain.ports;

import order_placement.domain.entities.Order;

public interface OrderRepository {
    void save(Order order);
    Order findById(String id);
}
```

**Fixes:**
- The port is defined in the Use Cases layer, not in the adapters. **Rule:** R-001, R-019.
- No dependency on Spring Data JPA. **Rule:** R-012.
- The name describes the business need (`OrderRepository`), not the technology. **Principle:** Screaming Architecture.

---

### Step 5: Create the Adapter (Humble Object)

```java
// AFTER: order_placement/adapters/persistence/JpaOrderRepository.java
package order_placement.adapters.persistence;

import order_placement.domain.entities.Order;
import order_placement.domain.ports.OrderRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
public class JpaOrderRepository implements OrderRepository {
    private final SpringDataOrderRepository springDataRepo;
    private final OrderEntityMapper mapper;

    public JpaOrderRepository(SpringDataOrderRepository springDataRepo, OrderEntityMapper mapper) {
        this.springDataRepo = springDataRepo;
        this.mapper = mapper;
    }

    @Override
    @Transactional
    public void save(Order order) {
        OrderEntity entity = mapper.toEntity(order);
        springDataRepo.save(entity);
    }

    @Override
    public Order findById(String id) {
        OrderEntity entity = springDataRepo.findById(id).orElse(null);
        return mapper.toDomain(entity);
    }
}
```

```java
// AFTER: order_placement/adapters/persistence/OrderEntity.java
package order_placement.adapters.persistence;

import javax.persistence.*;

@Entity
@Table(name = "orders")
public class OrderEntity {
    @Id
    private String id;

    @Column(name = "customer_id")
    private String customerId;

    @Column(name = "total")
    private double total;

    // Getters and setters...
}
```

```java
// AFTER: order_placement/adapters/persistence/OrderEntityMapper.java
package order_placement.adapters.persistence;

import order_placement.domain.entities.Order;

public class OrderEntityMapper {
    public OrderEntity toEntity(Order order) {
        OrderEntity entity = new OrderEntity();
        entity.setId(order.getId());
        entity.setCustomerId(order.getCustomerId());
        entity.setTotal(order.getTotal());
        return entity;
    }

    public Order toDomain(OrderEntity entity) {
        return new Order(entity.getId(), entity.getCustomerId(), /* lines */ null);
    }
}
```

**Fixes:**
- JPA annotations are moved to the adapter layer. **Rule:** R-011, R-012.
- The adapter implements the `OrderRepository` port. **Rule:** R-001.
- The adapter is a Humble Object — it is tied to JPA but delegates all logic to the Entity and Use Case. **Pattern:** Humble Object Pattern.
- `@Transactional` is in the adapter, not the use case. **Rule:** R-016.

---

### Step 6: Clean the Controller (Humble Object)

```java
// AFTER: order_placement/adapters/web/OrderController.java
package order_placement.adapters.web;

import order_placement.domain.usecases.PlaceOrder;
import order_placement.domain.usecases.PlaceOrderRequest;
import order_placement.domain.usecases.PlaceOrderResponse;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/orders")
public class OrderController {
    private final PlaceOrder placeOrder;
    private final OrderPresenter presenter;

    public OrderController(PlaceOrder placeOrder, OrderPresenter presenter) {
        this.placeOrder = placeOrder;
        this.presenter = presenter;
    }

    @PostMapping
    public OrderViewModel placeOrder(@RequestBody OrderInput input) {
        PlaceOrderRequest request = new PlaceOrderRequest(input.getId(), input.getCustomerId(), input.getLines());
        PlaceOrderResponse response = placeOrder.execute(request);
        return presenter.present(response);
    }
}
```

```java
// AFTER: order_placement/adapters/web/OrderPresenter.java
package order_placement.adapters.web;

import order_placement.domain.usecases.PlaceOrderResponse;

public class OrderPresenter {
    public OrderViewModel present(PlaceOrderResponse response) {
        return new OrderViewModel(response.getOrderId(), response.getTotal());
    }
}
```

```java
// AFTER: order_placement/adapters/web/OrderViewModel.java
package order_placement.adapters.web;

public class OrderViewModel {
    private final String orderId;
    private final double total;

    public OrderViewModel(String orderId, double total) {
        this.orderId = orderId;
        this.total = total;
    }

    // Getters...
}
```

**Fixes:**
- The controller converts HTTP input to a simple Request Model. **Rule:** R-004.
- The controller is a Humble Object — it only converts and delegates. **Pattern:** Humble Object Pattern.
- The Presenter formats the Response Model into a View Model. **Pattern:** Presenter/View.

---

### Step 7: Main Component (Wiring)

```java
// AFTER: main/EcommerceApplication.java
package main;

import order_placement.adapters.persistence.JpaOrderRepository;
import order_placement.adapters.persistence.OrderEntityMapper;
import order_placement.adapters.persistence.SpringDataOrderRepository;
import order_placement.adapters.web.OrderController;
import order_placement.adapters.web.OrderPresenter;
import order_placement.domain.ports.OrderRepository;
import order_placement.domain.usecases.PlaceOrder;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = {
    "order_placement.adapters",
    "main"
})
public class EcommerceApplication {
    public static void main(String[] args) {
        SpringApplication.run(EcommerceApplication.class, args);
    }

    @Bean
    public OrderRepository orderRepository(SpringDataOrderRepository springDataRepo, OrderEntityMapper mapper) {
        return new JpaOrderRepository(springDataRepo, mapper);
    }

    @Bean
    public PlaceOrder placeOrder(OrderRepository orderRepository) {
        return new PlaceOrder(orderRepository);
    }

    @Bean
    public OrderController orderController(PlaceOrder placeOrder, OrderPresenter presenter) {
        return new OrderController(placeOrder, presenter);
    }

    @Bean
    public OrderPresenter orderPresenter() {
        return new OrderPresenter();
    }

    @Bean
    public OrderEntityMapper orderEntityMapper() {
        return new OrderEntityMapper();
    }
}
```

**Fixes:**
- Main is the only place where Spring is mentioned. **Rule:** R-055.
- Main creates the factories and wires everything together. **Pattern:** Abstract Factory / Dependency Injection.
- Main is in the outermost circle. Everything else is clean. **Rule:** R-001.

---

## Summary of Violations and Fixes

| Violation | Rules Broken | Fix | Rules Applied |
|-----------|------------|-----|---------------|
| Framework-Centric directory structure | R-057, R-039 | Reorganize by use case | R-057, R-039 |
| JPA annotations in Entity | R-012, R-011, R-001 | Remove annotations; move to adapter | R-012, R-011, R-001 |
| Spring annotations in Service | R-012, R-016 | Remove annotations; extract Use Case | R-012, R-016 |
| Service depends on JpaRepository | R-006, R-001 | Define port in Use Cases layer; adapter implements it | R-006, R-001 |
| Controller passes DTO to Service | R-004 | Controller converts to Request Model | R-004 |
| Repository extends JpaRepository | R-012, R-001 | Port is pure interface; adapter wraps JpaRepository | R-012, R-001 |
| Business logic mixed with @Transactional | R-016 | Move @Transactional to adapter | R-016 |
| No Humble Object pattern | R-037 | Apply Presenter/View and Database Gateway patterns | R-037 |
| Main is not the only place with Spring | R-055 | Move all Spring wiring to Main | R-055 |

---

## Testability Improvement

**BEFORE:**
- Testing `OrderService` requires a Spring context, a database, and JPA.
- Tests are slow and brittle.

**AFTER:**
- `PlaceOrder` is tested with a mock `OrderRepository`.
- No Spring, no database, no web server.
- Tests are fast and stable. **Rule:** R-037, R-038.

```java
// Test the Use Case without Spring or the database.
@Test
public void testPlaceOrder() {
    OrderRepository repo = mock(OrderRepository.class);
    PlaceOrder useCase = new PlaceOrder(repo);
    PlaceOrderRequest request = new PlaceOrderRequest("order-1", "customer-1",
        List.of(new OrderLine("product-1", 2, 50.0)));

    PlaceOrderResponse response = useCase.execute(request);

    assertEquals("order-1", response.getOrderId());
    assertEquals(100.0, response.getTotal());
    verify(repo).save(any(Order.class));
}
```

---

## Key Takeaway

The refactor does not change the behavior of the system. It still places orders, calculates totals, and persists to the database. What changes is the **shape** of the system:
- The business rules are independent of the framework, database, and web.
- The architecture screams "E-Commerce!" not "Spring!"
- The system is testable, maintainable, and ready for change.

This is the essence of sound architecture: **The only way to go fast, is to go well.**
