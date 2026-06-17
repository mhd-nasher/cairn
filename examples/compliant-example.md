# Compliant Example: Order Processing System

> This is a worked example of a system that follows the Cairn canon. It shows how sound architecture is applied to a realistic order processing domain.

---

## System Overview

The system is an **Order Processing** service. It allows customers to place orders, calculates totals, applies discounts, and persists orders to a database. The system can be delivered via a REST API today and a mobile app tomorrow without changing the business rules.

---

## Top-Level Directory Structure (Screaming Architecture)

```
order-processing/
├── order_placement/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── Order.java
│   │   ├── usecases/
│   │   │   ├── PlaceOrder.java
│   │   │   ├── CalculateTotal.java
│   │   │   └── ApplyDiscount.java
│   │   └── ports/
│   │       ├── OrderRepository.java
│   │       └── DiscountService.java
│   ├── adapters/
│   │   ├── persistence/
│   │   │   ├── SqlOrderRepository.java
│   │   │   └── OrderMapper.java
│   │   ├── web/
│   │   │   ├── OrderController.java
│   │   │   └── OrderPresenter.java
│   │   └── external/
│   │       └── HttpDiscountService.java
│   └── config/
│       └── OrderPlacementConfig.java
├── billing/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── Invoice.java
│   │   ├── usecases/
│   │   │   └── GenerateInvoice.java
│   │   └── ports/
│   │       └── InvoiceRepository.java
│   ├── adapters/
│   │   ├── persistence/
│   │   │   └── SqlInvoiceRepository.java
│   │   └── web/
│   │       └── InvoiceController.java
│   └── config/
│       └── BillingConfig.java
├── shipping/
│   └── ... (similar structure)
└── main/
    └── Main.java
```

**Why this structure screams intent:**
- The top-level directories are `order_placement/`, `billing/`, `shipping/` — business functions.
- You can tell what the system does without opening a single file.
- There is no `controllers/`, `models/`, `views/` at the top level. **Rule:** R-057.

---

## Entities (Innermost Circle)

```java
// order_placement/domain/entities/Order.java
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

**Why this is compliant:**
- The Entity knows nothing about the database, web, or frameworks. **Rule:** R-001, R-002.
- There are no framework annotations (`@Entity`, `@Table`). **Rule:** R-012.
- There are no database imports. **Rule:** R-011.
- The Entity contains business rules (calculate total, apply discount). **Principle:** Entities are enterprise-wide critical business rules.

---

## Use Cases (Second Circle)

```java
// order_placement/domain/usecases/PlaceOrder.java
package order_placement.domain.usecases;

import order_placement.domain.entities.Order;
import order_placement.domain.ports.OrderRepository;
import order_placement.domain.ports.DiscountService;

public class PlaceOrder {
    private final OrderRepository orderRepository;
    private final DiscountService discountService;

    public PlaceOrder(OrderRepository orderRepository, DiscountService discountService) {
        this.orderRepository = orderRepository;
        this.discountService = discountService;
    }

    public PlaceOrderResponse execute(PlaceOrderRequest request) {
        Order order = new Order(request.getId(), request.getCustomerId(), request.getLines());
        order.calculateTotal();
        double discountRate = discountService.getDiscountRate(request.getCustomerId());
        order.applyDiscount(discountRate);
        orderRepository.save(order);
        return new PlaceOrderResponse(order.getId(), order.getTotal());
    }
}
```

```java
// order_placement/domain/usecases/PlaceOrderRequest.java
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
// order_placement/domain/usecases/PlaceOrderResponse.java
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

**Why this is compliant:**
- The Use Case depends on the Entity and on abstract ports (`OrderRepository`, `DiscountService`). **Rule:** R-001, R-006.
- The Use Case does not know about SQL, HTTP, or frameworks. **Rule:** R-011, R-030, R-012.
- The Request and Response are simple data structures (DTOs). **Rule:** R-004.
- The Use Case is testable without the database or web. **Rule:** R-037.

---

## Ports (Interfaces in the Use Cases Layer)

```java
// order_placement/domain/ports/OrderRepository.java
package order_placement.domain.ports;

import order_placement.domain.entities.Order;

public interface OrderRepository {
    void save(Order order);
    Order findById(String id);
}
```

```java
// order_placement/domain/ports/DiscountService.java
package order_placement.domain.ports;

public interface DiscountService {
    double getDiscountRate(String customerId);
}
```

**Why this is compliant:**
- The ports are defined in the Use Cases layer, not in the adapters. **Rule:** R-001, R-019.
- The port names describe the business need (`OrderRepository`, `DiscountService`), not the technology (`SqlOrderDao`, `HttpDiscountClient`). **Principle:** Screaming Architecture.
- The ports use simple data structures (Entity, String, double). **Rule:** R-004.

---

## Adapters (Third Circle)

### Persistence Adapter (Humble Object)

```java
// order_placement/adapters/persistence/SqlOrderRepository.java
package order_placement.adapters.persistence;

import order_placement.domain.entities.Order;
import order_placement.domain.ports.OrderRepository;

public class SqlOrderRepository implements OrderRepository {
    private final JdbcTemplate jdbcTemplate; // Framework-specific, but only here

    public SqlOrderRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public void save(Order order) {
        // SQL is restricted to the adapter layer. Rule: R-011.
        jdbcTemplate.update("INSERT INTO orders (id, customer_id, total) VALUES (?, ?, ?)",
            order.getId(), order.getCustomerId(), order.getTotal());
    }

    @Override
    public Order findById(String id) {
        // SQL is restricted to the adapter layer. Rule: R-011.
        return jdbcTemplate.queryForObject(
            "SELECT * FROM orders WHERE id = ?",
            new OrderMapper(), id);
    }
}
```

```java
// order_placement/adapters/persistence/OrderMapper.java
package order_placement.adapters.persistence;

import order_placement.domain.entities.Order;
import org.springframework.jdbc.core.RowMapper;
import java.sql.ResultSet;
import java.sql.SQLException;

public class OrderMapper implements RowMapper<Order> {
    @Override
    public Order mapRow(ResultSet rs, int rowNum) throws SQLException {
        // Maps database representation to Entity.
        // The Entity knows nothing about the mapper. Rule: R-001, R-011.
        return new Order(rs.getString("id"), rs.getString("customer_id"), /* lines */ null);
    }
}
```

**Why this is compliant:**
- SQL is restricted to the adapter layer. **Rule:** R-011.
- The adapter implements a port defined in the Use Cases layer. **Rule:** R-001.
- The adapter is a Humble Object — it is tied to the database and hard to test, but it delegates all logic to the Entity and Use Case. **Pattern:** Humble Object Pattern.

### Web Adapter (Humble Object)

```java
// order_placement/adapters/web/OrderController.java
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
        // Convert HTTP input to Request Model.
        PlaceOrderRequest request = new PlaceOrderRequest(input.getId(), input.getCustomerId(), input.getLines());
        PlaceOrderResponse response = placeOrder.execute(request);
        // Convert Response Model to View Model.
        return presenter.present(response);
    }
}
```

```java
// order_placement/adapters/web/OrderPresenter.java
package order_placement.adapters.web;

import order_placement.domain.usecases.PlaceOrderResponse;

public class OrderPresenter {
    public OrderViewModel present(PlaceOrderResponse response) {
        return new OrderViewModel(response.getOrderId(), response.getTotal());
    }
}
```

```java
// order_placement/adapters/web/OrderViewModel.java
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

**Why this is compliant:**
- The Controller is a Humble Object — it only converts HTTP to Request/Response models and delegates to the Use Case. **Pattern:** Humble Object Pattern.
- The Controller does not contain business logic. **Rule:** R-001.
- The Presenter formats the Response Model into a View Model. **Pattern:** Presenter/View.
- The Use Case does not know about HTTP, JSON, or Spring. **Rule:** R-030, R-012.

---

## Main Component (Outermost Circle)

```java
// main/Main.java
package main;

import order_placement.adapters.persistence.SqlOrderRepository;
import order_placement.adapters.web.OrderController;
import order_placement.adapters.web.OrderPresenter;
import order_placement.domain.usecases.PlaceOrder;
import order_placement.domain.ports.OrderRepository;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }

    @Bean
    public OrderRepository orderRepository(JdbcTemplate jdbcTemplate) {
        return new SqlOrderRepository(jdbcTemplate);
    }

    @Bean
    public PlaceOrder placeOrder(OrderRepository orderRepository) {
        return new PlaceOrder(orderRepository, /* discountService */ null);
    }

    @Bean
    public OrderController orderController(PlaceOrder placeOrder, OrderPresenter presenter) {
        return new OrderController(placeOrder, presenter);
    }

    @Bean
    public OrderPresenter orderPresenter() {
        return new OrderPresenter();
    }
}
```

**Why this is compliant:**
- Main is the only place where Spring is mentioned. **Rule:** R-055.
- Main creates the factories and wires everything together. **Pattern:** Abstract Factory / Dependency Injection.
- Main is in the outermost circle. Everything else is clean. **Rule:** R-001, R-012.

---

## Testing

```java
// Test the Use Case without the database or web.
package order_placement.domain.usecases;

import order_placement.domain.entities.Order;
import order_placement.domain.ports.OrderRepository;
import order_placement.domain.ports.DiscountService;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class PlaceOrderTest {
    @Test
    public void testPlaceOrder() {
        OrderRepository repo = mock(OrderRepository.class);
        DiscountService discount = mock(DiscountService.class);
        when(discount.getDiscountRate("customer-1")).thenReturn(0.1);

        PlaceOrder useCase = new PlaceOrder(repo, discount);
        PlaceOrderRequest request = new PlaceOrderRequest("order-1", "customer-1",
            List.of(new OrderLine("product-1", 2, 50.0)));

        PlaceOrderResponse response = useCase.execute(request);

        assertEquals("order-1", response.getOrderId());
        assertEquals(90.0, response.getTotal()); // 2 * 50 = 100, minus 10% = 90
        verify(repo).save(any(Order.class));
    }
}
```

**Why this is compliant:**
- The test does not use the database, web, or framework. **Rule:** R-037, R-038.
- The test is fast and stable. **Principle:** Tests as System Components.
- The test uses mocks for the ports. **Pattern:** Humble Object Pattern.

---

## Summary of Compliance

| Principle/Rule | How This Example Satisfies It |
|----------------|-------------------------------|
| R-001 (Dependency Rule) | All dependencies point inward. |
| R-011 (No SQL in Use Cases) | SQL is restricted to `SqlOrderRepository`. |
| R-030 (Web Is an IO Device) | HTTP is restricted to `OrderController`. |
| R-012 (No Frameworks in Core) | No Spring annotations in Entities or Use Cases. |
| R-057 (Screaming Architecture) | Top-level directories are `order_placement/`, `billing/`, `shipping/`. |
| R-039 (Use Cases Divide System) | Each use case has its own package. |
| R-037 (Testability Without GUI) | Use Cases are tested with mocks. |
| R-055 (Main Is Ultimate Detail) | `Main.java` is the only place where Spring is mentioned. |
| R-006 (DIP) | Use Cases depend on `OrderRepository` interface, not `SqlOrderRepository`. |
| R-016 (SRP) | `Order` handles business rules; `PlaceOrder` handles the use case; `SqlOrderRepository` handles persistence. |
| R-018 (OCP) | New adapters can be added without changing Use Cases or Entities. |
| R-028 (Leave Decoupling Mode Open) | The system can be deployed as a monolith or as services without changing the business rules. |
