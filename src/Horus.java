import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import java.io.*;
import java.lang.Runtime;
 
public class Horus extends Application {
    public static void main(String[] args) {
        launch(args);
    }
    
    Image img = new Image("ui_img/startscreen.jpg");
    Image horus = new Image("ui_img/Horus.png");
    Image start = new Image("ui_img/start.png");
    Image horusName = new Image("ui_img/HorusName.png");
    Image chooseMode = new Image("ui_img/choosemode.png");
    Image singleUser = new Image("ui_img/singleuser.png");
    Image crowdControl = new Image("ui_img/crowdcontrol.png");
    Image deceptionDetection = new Image("ui_img/deceptiondetection.png");
    Image lastAnalyses = new Image("ui_img/lastanalyses.png");
    Image screenCapture = new Image("ui_img/screencaptıure.png");
    Image back = new Image("ui_img/backButton.png");

    BackgroundSize backgroundSize = new BackgroundSize(100, 100, true, true, true, true);
    BackgroundImage bImg = new BackgroundImage(img, BackgroundRepeat.NO_REPEAT, BackgroundRepeat.NO_REPEAT, BackgroundPosition.DEFAULT, backgroundSize);
    Background bGround = new Background(bImg);
    
    Button startButton = new Button();
    Button singleUserButton = new Button();
    Button crowdControlButton = new Button();
    Button deceptionDetectionButton = new Button();
    Button lastAnalysesButton = new Button();
    Button screenCaptureButton = new Button();
    Button backButton = new Button();
    
    ImageView horusView = new ImageView(horus); 
    ImageView startButtonView = new ImageView(start);
    ImageView horusNameView = new ImageView(horusName);
    ImageView chooseModeView = new ImageView(chooseMode);
    ImageView singleUserView = new ImageView(singleUser);
    ImageView crowdControlView = new ImageView(crowdControl);
    ImageView deceptionDetectionView = new ImageView(deceptionDetection);
    ImageView lastAnalysesView = new ImageView(lastAnalyses);
    ImageView screenCaptureView = new ImageView(screenCapture);
    ImageView backButtonView = new ImageView(back);
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @Override
    public void start(Stage primaryStage) {
        
        primaryStage.setTitle("Horus");
        Scene startScene = new Scene(startScreenVBox(), 870, 570);
        primaryStage.setScene(startScene);
        primaryStage.setMaximized(true); 
        primaryStage.show();
    }
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    public VBox startScreenVBox()
    {
        horusView.setPreserveRatio(true);
        horusNameView.setPreserveRatio(true);
        startButton.setGraphic(startButtonView);
        startButton.setStyle("-fx-background-color: transparent;");
        
        startButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event) 
            {
                startButton.getScene().setRoot(modeScreenVBox());
            }
        });

        VBox root = new VBox();
        root.setBackground(bGround);
        root.setAlignment(Pos.CENTER);
        root.getChildren().add(horusView);
        root.getChildren().add(horusNameView);
        root.getChildren().add(startButton);
        return root;
    }
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    public VBox modeScreenVBox()
    {
        horusView.setPreserveRatio(true);
        horusNameView.setPreserveRatio(true);
        chooseModeView.setPreserveRatio(true);

        singleUserButton.setGraphic(singleUserView);
        crowdControlButton.setGraphic(crowdControlView);
        deceptionDetectionButton.setGraphic(deceptionDetectionView);
        lastAnalysesButton.setGraphic(lastAnalysesView);
        screenCaptureButton.setGraphic(screenCaptureView);

        singleUserButton.setStyle("-fx-background-color: transparent;");
        crowdControlButton.setStyle("-fx-background-color: transparent;");
        deceptionDetectionButton.setStyle("-fx-background-color: transparent;");
        lastAnalysesButton.setStyle("-fx-background-color: transparent;");
        screenCaptureButton.setStyle("-fx-background-color: transparent;");
        
        horusView.setFitHeight(150);
        horusView.setFitWidth(150);
        horusNameView.setFitHeight(200);
        horusNameView.setFitWidth(200);
        chooseModeView.setFitHeight(400);
        chooseModeView.setFitWidth(400);
        
        singleUserButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event) 
            {
                singleUserButton.getScene().setRoot(singleUserVBox());
            }
        });

        crowdControlButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event) 
            {
                crowdControlButton.getScene().setRoot(crowdControlVBox());
            }
        });

        deceptionDetectionButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event) 
            {
                deceptionDetectionButton.getScene().setRoot(deceptionDetectionVBox());
            }
        });

        screenCaptureButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event) 
            {
                screenCaptureButton.getScene().setRoot(screenCaptureVBox());
            }
        });

        lastAnalysesButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event) 
            {
                lastAnalysesButton.getScene().setRoot(lastAnalysesVBox());
            }
        });

        VBox root = new VBox();
        root.setBackground(bGround);
        root.setAlignment(Pos.CENTER);
        root.getChildren().add(horusView);
        root.getChildren().add(horusNameView);
        root.getChildren().add(chooseModeView);
        root.getChildren().add(singleUserButton);
        root.getChildren().add(deceptionDetectionButton);
        root.getChildren().add(crowdControlButton);
        root.getChildren().add(screenCaptureButton);
        root.getChildren().add(lastAnalysesButton);
        return root;
    }
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    public VBox singleUserVBox()
    {
        backButton.setGraphic(backButtonView);
        backButton.setStyle("-fx-background-color: transparent;");
        
        backButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event)
            {
                backButton.getScene().setRoot(modeScreenVBox());
            }
        });
        

        VBox root = new VBox();
        root.setBackground(bGround);
        
        root.getChildren().add(backButton);
        return root;
    }
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    public VBox crowdControlVBox()
    {
        backButton.setGraphic(backButtonView);
        backButton.setStyle("-fx-background-color: transparent;");
        try{
            Process p = Runtime.getRuntime().exec("python faces.py");
        } catch(IOException e){
            e.printStackTrace();
        }
        backButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event)
            {
                backButton.getScene().setRoot(modeScreenVBox());
            }
        });

        VBox root = new VBox();
        root.setBackground(bGround);
        
        root.getChildren().add(backButton);
        return root;
    }
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    public VBox deceptionDetectionVBox()
    {
        backButton.setGraphic(backButtonView);
        backButton.setStyle("-fx-background-color: transparent;");

        backButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event)
            {
                backButton.getScene().setRoot(modeScreenVBox());
            }
        });

        VBox root = new VBox();
        root.setBackground(bGround);
        
        root.getChildren().add(backButton);
        return root;
    }
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    public VBox screenCaptureVBox()
    {
        backButton.setGraphic(backButtonView);
        backButton.setStyle("-fx-background-color: transparent;");

        backButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event)
            {
                backButton.getScene().setRoot(modeScreenVBox());
            }
        });

        VBox root = new VBox();
        root.setBackground(bGround);
        
        root.getChildren().add(backButton);
        return root;
    }
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    public VBox lastAnalysesVBox()
    {
        backButton.setGraphic(backButtonView);
        backButton.setStyle("-fx-background-color: transparent;");
        
        backButton.setOnAction(new EventHandler<ActionEvent>() 
        {
            @Override
            public void handle(ActionEvent event)
            {
                backButton.getScene().setRoot(modeScreenVBox());
            }
        });

        VBox root = new VBox();
        root.setBackground(bGround);
        
        root.getChildren().add(backButton);
        return root;
    }

}