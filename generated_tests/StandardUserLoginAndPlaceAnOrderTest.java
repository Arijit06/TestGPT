package com.testgpt.generated;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import java.time.Duration;

/**
 * This class contains end-to-end tests for a standard user to login and place an order.
 */
public class StandardUserLoginAndPlaceAnOrderTest {

    private WebDriver driver;
    private WebDriverWait wait;
    private static final String BASE_URL = "https://www.saucedemo.com";
    private static final String USERNAME = "standard_user";
    private static final String PASSWORD = "secret_sauce";

    @BeforeMethod
    public void setUp() {
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        driver.get(BASE_URL);
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    public void testMainScenario() {
        // Arrange
        WebElement usernameField = wait.until(ExpectedConditions.elementToBeClickable(By.id("user-name")));
        WebElement passwordField = wait.until(ExpectedConditions.elementToBeClickable(By.id("password")));
        WebElement loginButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("login-button")));
        // Act
        usernameField.sendKeys(USERNAME);
        passwordField.sendKeys(PASSWORD);
        loginButton.click();
        // Wait for inventory page to load
        wait.until(ExpectedConditions.urlContains("inventory.html"));
        // Add to cart
        WebElement addToCartButton = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//button[@id='add-to-cart-sauce-labs-backpack']")));
        addToCartButton.click();
        // Click shopping cart icon
        WebElement shoppingCartIcon = wait.until(ExpectedConditions.elementToBeClickable(By.className("shopping_cart_link")));
        shoppingCartIcon.click();
        // Click Checkout
        WebElement checkoutButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("checkout")));
        checkoutButton.click();
        // Fill in checkout form
        WebElement firstNameField = wait.until(ExpectedConditions.elementToBeClickable(By.id("first-name")));
        WebElement lastNameField = wait.until(ExpectedConditions.elementToBeClickable(By.id("last-name")));
        WebElement zipCodeField = wait.until(ExpectedConditions.elementToBeClickable(By.id("postal-code")));
        WebElement continueButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("continue")));
        firstNameField.sendKeys("John");
        lastNameField.sendKeys("Doe");
        zipCodeField.sendKeys("12345");
        continueButton.click();
        // Click Finish
        WebElement finishButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("finish")));
        finishButton.click();
        // Assert
        WebElement confirmationMessage = wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("complete-header")));
        Assert.assertTrue(confirmationMessage.isDisplayed());
        Assert.assertEquals(confirmationMessage.getText(), "THANK YOU FOR YOUR ORDER");
    }

    @Test
    public void testEdgeCase_CartAlreadyHasItems() {
        // Arrange
        WebElement usernameField = wait.until(ExpectedConditions.elementToBeClickable(By.id("user-name")));
        WebElement passwordField = wait.until(ExpectedConditions.elementToBeClickable(By.id("password")));
        WebElement loginButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("login-button")));
        // Act
        usernameField.sendKeys(USERNAME);
        passwordField.sendKeys(PASSWORD);
        loginButton.click();
        // Wait for inventory page to load
        wait.until(ExpectedConditions.urlContains("inventory.html"));
        // Add to cart
        WebElement addToCartButton = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//button[@id='add-to-cart-sauce-labs-backpack']")));
        addToCartButton.click();
        // Add another item to cart
        WebElement addToCartButton2 = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//button[@id='add-to-cart-sauce-labs-bike-light']")));
        addToCartButton2.click();
        // Click shopping cart icon
        WebElement shoppingCartIcon = wait.until(ExpectedConditions.elementToBeClickable(By.className("shopping_cart_link")));
        shoppingCartIcon.click();
        // Assert
        WebElement cartItemCount = wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("cart_quantity")));
        Assert.assertTrue(cartItemCount.isDisplayed());
        Assert.assertEquals(cartItemCount.getText(), "2");
    }

    @Test
    public void testEdgeCase_CheckoutFormSubmittedWithEmptyFields() {
        // Arrange
        WebElement usernameField = wait.until(ExpectedConditions.elementToBeClickable(By.id("user-name")));
        WebElement passwordField = wait.until(ExpectedConditions.elementToBeClickable(By.id("password")));
        WebElement loginButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("login-button")));
        // Act
        usernameField.sendKeys(USERNAME);
        passwordField.sendKeys(PASSWORD);
        loginButton.click();
        // Wait for inventory page to load
        wait.until(ExpectedConditions.urlContains("inventory.html"));
        // Add to cart
        WebElement addToCartButton = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//button[@id='add-to-cart-sauce-labs-backpack']")));
        addToCartButton.click();
        // Click shopping cart icon
        WebElement shoppingCartIcon = wait.until(ExpectedConditions.elementToBeClickable(By.className("shopping_cart_link")));
        shoppingCartIcon.click();
        // Click Checkout
        WebElement checkoutButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("checkout")));
        checkoutButton.click();
        // Submit checkout form with empty fields
        WebElement continueButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("continue")));
        continueButton.click();
        // Assert
        WebElement errorMessages = wait.until(ExpectedConditions.visibilityOfAllElementsLocatedBy(By.xpath("//input[@class='error']")));
        Assert.assertTrue(errorMessages.size() > 0);
    }

    @Test
    public void testEdgeCase_FirstProductOutOfStock() {
        // Arrange
        WebElement usernameField = wait.until(ExpectedConditions.elementToBeClickable(By.id("user-name")));
        WebElement passwordField = wait.until(ExpectedConditions.elementToBeClickable(By.id("password")));
        WebElement loginButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("login-button")));
        // Act
        usernameField.sendKeys(USERNAME);
        passwordField.sendKeys(PASSWORD);
        loginButton.click();
        // Wait for inventory page to load
        wait.until(ExpectedConditions.urlContains("inventory.html"));
        // Try to add out of stock product to cart
        try {
            WebElement addToCartButton = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//button[@id='add-to-cart-sauce-labs-onesie']")));
            addToCartButton.click();
        } catch (Exception e) {
            // Ignore exception if product is out of stock
        }
        // Assert
        WebElement cartItemCount = wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("cart_quantity")));
        Assert.assertTrue(cartItemCount.isDisplayed());
        Assert.assertEquals(cartItemCount.getText(), "0");
    }
}