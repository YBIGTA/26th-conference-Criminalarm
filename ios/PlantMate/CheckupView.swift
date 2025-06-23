import SwiftUI

struct CheckupView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var currentStep: CheckupStep = .initial
    @State private var isAnalyzing = false
    @State private var showResult = false
    @State private var selectedImage: UIImage?
    @State private var showImagePicker = false
    @State private var showMenu = false
    
    enum CheckupStep {
        case initial        // 사진 업로드 대기
        case analyzing      // 진단 중
        case result         // 결과 표시
    }
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Background
                Color(red: 234/255, green: 230/255, blue: 213/255)
                    .ignoresSafeArea()
                
                VStack(spacing: 0) {
                    // Status Bar 영역
                    Rectangle()
                        .fill(Color.clear)
                        .frame(height: 62)
                    
                    // Header
                    HStack {
                        // Back Button
                        Button(action: {
                            dismiss()
                        }) {
                            Image(systemName: "chevron.left")
                                .font(.system(size: 20, weight: .medium))
                                .foregroundColor(.black)
                        }
                        
                        Spacer()
                        
                        Text("Checkup")
                            .font(.system(size: 32, weight: .regular, design: .rounded))
                            .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                        
                        Spacer()
                        
                        Button(action: {
                            showMenu = true
                        }) {
                            Image(systemName: "line.3.horizontal")
                                .font(.system(size: 24))
                                .foregroundColor(.black)
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.bottom, 30)
                    
                    // Content based on current step
                    switch currentStep {
                    case .initial:
                        InitialCheckupView(onCameraButtonTapped: {
                            showImagePicker = true
                        })
                        
                    case .analyzing:
                        AnalyzingCheckupView()
                        
                    case .result:
                        ResultCheckupView()
                    }
                    
                    Spacer()
                    
                    // Home Indicator 영역
                    Rectangle()
                        .fill(Color.clear)
                        .frame(height: 34)
                }
            }
        }
        .navigationBarHidden(true)
        .sheet(isPresented: $showImagePicker) {
            ImagePickerView(selectedImage: $selectedImage) { image in
                if image != nil {
                    currentStep = .analyzing
                    
                    // 2초 후 결과 화면으로 이동
                    DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
                        currentStep = .result
                    }
                }
            }
        }
        .overlay(
            // Menu Overlay
            Group {
                if showMenu {
                    MenuView(
                        isPresented: $showMenu,
                        onChatTapped: {
                            // 채팅 화면으로 이동 (필요시 구현)
                        },
                        onReportTapped: {
                            // 리포트 화면으로 이동 (필요시 구현)
                        },
                        onCheckupTapped: {
                            // 이미 체크업 화면이므로 아무것도 하지 않음
                        }
                    )
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .trailing).combined(with: .opacity)
                    ))
                    .animation(.easeInOut(duration: 0.3), value: showMenu)
                    .zIndex(1)
                }
            }
        )
    }
}

// MARK: - Initial Checkup View (사진 업로드 대기)
struct InitialCheckupView: View {
    let onCameraButtonTapped: () -> Void
    
    var body: some View {
        VStack(spacing: 40) {
            // Upload Area
            Button(action: onCameraButtonTapped) {
                VStack(spacing: 20) {
                    // Dashed Border Container
                    RoundedRectangle(cornerRadius: 15)
                        .stroke(Color(red: 3/255, green: 158/255, blue: 8/255), style: StrokeStyle(lineWidth: 4, dash: [8]))
                        .frame(width: 309, height: 196)
                        .background(Color.white)
                        .cornerRadius(15)
                        .overlay(
                            VStack(spacing: 16) {
                                // Camera Icon
                                Image(systemName: "camera.fill")
                                    .font(.system(size: 60))
                                    .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                                
                                // Upload Text
                                VStack(spacing: 4) {
                                    Text("사진 업로드하여")
                                        .font(.system(size: 12, weight: .regular))
                                        .foregroundColor(.black)
                                    Text("상태 진단하기")
                                        .font(.system(size: 12, weight: .regular))
                                        .foregroundColor(.black)
                                }
                            }
                        )
                }
            }
            
            Spacer()
        }
        .padding(.horizontal, 20)
    }
}

// MARK: - Analyzing Checkup View (진단 중)
struct AnalyzingCheckupView: View {
    @State private var rotationAngle: Double = 0
    
    var body: some View {
        VStack(spacing: 40) {
            // Upload Area (같은 디자인 유지)
            RoundedRectangle(cornerRadius: 15)
                .stroke(Color(red: 3/255, green: 158/255, blue: 8/255), style: StrokeStyle(lineWidth: 4, dash: [8]))
                .frame(width: 309, height: 196)
                .background(Color.white)
                .cornerRadius(15)
            
            // Analysis Section
            VStack(spacing: 30) {
                // White Result Container
                VStack(spacing: 30) {
                    // Loading Icon with Animation
                    Image(systemName: "hourglass")
                        .font(.system(size: 90))
                        .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                        .rotationEffect(.degrees(rotationAngle))
                        .onAppear {
                            withAnimation(.linear(duration: 2.0).repeatForever(autoreverses: false)) {
                                rotationAngle = 360
                            }
                        }
                    
                    Text("반려식물을 진단하고 있어요")
                        .font(.system(size: 12, weight: .regular))
                        .foregroundColor(.black)
                }
                .frame(maxWidth: .infinity)
                .frame(height: 520)
                .background(Color.white)
                .cornerRadius(15)
                .padding(.horizontal, 14)
            }
            
            Spacer()
        }
        .padding(.horizontal, 20)
    }
}

// MARK: - Result Checkup View (진단 완료)
struct ResultCheckupView: View {
    var body: some View {
        VStack(spacing: 40) {
            // Upload Area (같은 디자인 유지)
            RoundedRectangle(cornerRadius: 15)
                .stroke(Color(red: 3/255, green: 158/255, blue: 8/255), style: StrokeStyle(lineWidth: 4, dash: [8]))
                .frame(width: 309, height: 196)
                .background(Color.white)
                .cornerRadius(15)
                .overlay(
                    VStack(spacing: 16) {
                        // Camera Icon
                        Image(systemName: "camera.fill")
                            .font(.system(size: 60))
                            .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                        
                        // Upload Text
                        VStack(spacing: 4) {
                            Text("사진 업로드하여")
                                .font(.system(size: 12, weight: .regular))
                                .foregroundColor(.black)
                            Text("상태 진단하기")
                                .font(.system(size: 12, weight: .regular))
                                .foregroundColor(.black)
                        }
                    }
                )
            
            // Result Section
            VStack(spacing: 0) {
                // White Result Container
                VStack(alignment: .leading, spacing: 20) {
                    // Current Status Header
                    HStack {
                        Spacer()
                        Text("현재 상태")
                            .font(.system(size: 20, weight: .medium))
                            .foregroundColor(.black)
                        Spacer()
                    }
                    .padding(.top, 30)
                    
                    // Status Result
                    HStack {
                        Spacer()
                        Text("수분 부족")
                            .font(.system(size: 32, weight: .bold))
                            .foregroundColor(Color(red: 3/255, green: 158/255, blue: 8/255))
                        Spacer()
                    }
                    
                    Divider()
                        .padding(.vertical, 10)
                    
                    // Problem Causes
                    VStack(alignment: .leading, spacing: 12) {
                        HStack {
                            Circle()
                                .fill(Color.black)
                                .frame(width: 4, height: 4)
                            Text("문제 주요 원인")
                                .font(.system(size: 16, weight: .bold))
                                .foregroundColor(.black)
                        }
                        
                        Text("그리워하면 언젠가 만나게 되는\n어느 영화와 같은 일들이 이뤄져 가기를\n힘겨워 한 날에 너를 지킬 수 없었던\n아름다운 시절 속에 머문 그대이기에")
                            .font(.system(size: 14, weight: .regular))
                            .foregroundColor(.black)
                            .lineSpacing(4)
                            .padding(.leading, 16)
                    }
                    
                    // Solutions
                    VStack(alignment: .leading, spacing: 12) {
                        HStack {
                            Circle()
                                .fill(Color.black)
                                .frame(width: 4, height: 4)
                            Text("해결 방법")
                                .font(.system(size: 16, weight: .bold))
                                .foregroundColor(.black)
                        }
                        
                        Text("그리워하면 언젠가 만나게 되는\n어느 영화와 같은 일들이 이뤄져 가기를\n힘겨워 한 날에 너를 지킬 수 없었던\n아름다운 시절 속에 머문 그대여\n그리워하면 언젠가 만나게 되는\n어느 영화와 같은 일들이 이뤄져 가기를\n힘겨워 한 날에 너를 지킬 수 없었던\n아름다운 시절 속에 머문 그대이기에")
                            .font(.system(size: 14, weight: .regular))
                            .foregroundColor(.black)
                            .lineSpacing(4)
                            .padding(.leading, 16)
                    }
                    
                    Spacer()
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .frame(height: 520)
                .background(Color.white)
                .cornerRadius(15)
                .padding(.horizontal, 14)
            }
            
            Spacer()
        }
        .padding(.horizontal, 20)
    }
}

// MARK: - Image Picker
struct ImagePickerView: UIViewControllerRepresentable {
    @Binding var selectedImage: UIImage?
    let onImageSelected: (UIImage?) -> Void
    
    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.sourceType = .photoLibrary
        picker.allowsEditing = true
        picker.delegate = context.coordinator
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: ImagePickerView
        
        init(_ parent: ImagePickerView) {
            self.parent = parent
        }
        
        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.editedImage] as? UIImage ?? info[.originalImage] as? UIImage {
                parent.selectedImage = image
                parent.onImageSelected(image)
            }
            picker.dismiss(animated: true)
        }
        
        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.onImageSelected(nil)
            picker.dismiss(animated: true)
        }
    }
}

struct PlantCheckupCharacterView: View {
    @State private var bounce = false
    @State private var leafSway = false
    
    var body: some View {
        ZStack {
            // 화분 (황갈색 사다리꼴)
            Path { path in
                path.move(to: CGPoint(x: 8, y: 0))
                path.addLine(to: CGPoint(x: 32, y: 0))
                path.addLine(to: CGPoint(x: 37, y: 28))
                path.addLine(to: CGPoint(x: 3, y: 28))
                path.closeSubpath()
            }
            .fill(Color(red: 218/255, green: 165/255, blue: 32/255))
            .frame(width: 40, height: 28)
            .offset(y: 14)
            
            // 식물 머리 (베이지색 원)
            Circle()
                .fill(Color(red: 222/255, green: 184/255, blue: 135/255))
                .frame(width: 35, height: 35)
                .overlay(
                    // 눈 두 개
                    HStack(spacing: 7) {
                        Circle()
                            .fill(Color.black)
                            .frame(width: 2.5, height: 2.5)
                        Circle()
                            .fill(Color.black)
                            .frame(width: 2.5, height: 2.5)
                    }
                    .offset(y: -1)
                )
                .offset(y: bounce ? -1 : 1)
                .animation(.easeInOut(duration: 2.0).repeatForever(autoreverses: true), value: bounce)
            
            // 왼쪽 잎사귀
            Ellipse()
                .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                .frame(width: 9, height: 14)
                .rotationEffect(.degrees(-30))
                .offset(x: -11, y: -14)
                .rotationEffect(.degrees(leafSway ? -3 : 3))
                .animation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: leafSway)
            
            // 오른쪽 잎사귀
            Ellipse()
                .fill(Color(red: 34/255, green: 139/255, blue: 34/255))
                .frame(width: 9, height: 14)
                .rotationEffect(.degrees(30))
                .offset(x: 11, y: -14)
                .rotationEffect(.degrees(leafSway ? 3 : -3))
                .animation(.easeInOut(duration: 1.8).repeatForever(autoreverses: true), value: leafSway)
        }
        .frame(width: 45, height: 45)
        .onAppear {
            bounce = true
            leafSway = true
        }
    }
}

#Preview {
    CheckupView()
} 